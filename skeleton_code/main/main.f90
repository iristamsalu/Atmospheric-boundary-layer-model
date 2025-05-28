!+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
!
! Main program
!
! - Simulate emissions and chemical reactions of gases, aerosol processes as well as 
!   transport of gases and aerosol particles within the planetary boundary layer with a
!   column model.
! - Check Fortran conventions at http://www.fortran90.org/src/best-practices.html
! - Check code conventions at
!   http://www.cesm.ucar.edu/working_groups/Software/dev_guide/dev_guide/node7.html
!
!+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

program main
use chemistry_mod
use aerosol_mod
implicit none

!-----------------------------------------------------------------------------------------
! Control variables (can be moved to an input file in future)
!-----------------------------------------------------------------------------------------
logical :: use_emission   = .true.
logical :: use_chemistry  = .true.
logical :: use_deposition = .false.
logical :: use_aerosol    = .true.
character(len=255), parameter :: input_dir  = './input'
character(len=255), parameter :: output_dir = './output'
integer :: model_v = 3   ! Model version (1, 2 or 3) for meteorology

!-----------------------------------------------------------------------------------------
! Constants
!-----------------------------------------------------------------------------------------
! Double precision
! http://en.wikipedia.org/wiki/Double_precision_floating-point_format
! integer, parameter :: dp = selected_real_kind(15, 307)

! Physics constants
! real(dp), parameter :: PI     = 2*asin(1.0_dp)                  ! the constant pi
real(dp), parameter :: grav   = 9.81_dp                         ! [m s-2], gravitation
real(dp), parameter :: Rgas   = 8.3144598_dp                    ! [J mol-1 K-1], universal gas constant
real(dp), parameter :: NA     = 6.022140857e23_dp               ! [molec mol-1], Avogadro's number 
real(dp), parameter :: mm_air = 28.96e-3_dp                     ! [kg mol-1], mean molar mass of air
real(dp), parameter :: kb     = 1.38064852e-23_dp               ! [m2 kg s-2 K-1], Boltzmann constant
real(dp), parameter :: Cp     = 1012.0_dp                       ! [J kg-1 K-1], air specific heat at constant pressure,
real(dp), parameter :: p00    = 1.01325e5_dp                    ! [Pa], reference pressure at surface
real(dp), parameter :: nu_air = 1.59e-5_dp                      ! [m2 s-1], kinematic viscosity of air
real(dp), parameter :: Omega  = 2*PI/(24.0_dp*60.0_dp*60.0_dp)  ! [rad s-1], Earth angular speed
real(dp), parameter :: lambda = 300.0_dp                        ! maximum mixing length, meters
real(dp), parameter :: vonk   = 0.4_dp                          ! von Karman constant, dimensionless
real(dp), parameter :: ppb = 1e-9_dp

real(dp), parameter :: ug = 10.0d0, vg = 0.0d0  ! [m s-1], geostrophic wind

! Latitude and longitude of Hyltemossa
real(dp), parameter :: latitude_deg = 56.1d0 ! [degN]
real(dp), parameter :: longitude_deg = 13.42d0 ! [degE]
real(dp), parameter :: latitude      = latitude_deg  * PI/180.0d0  ! [rad]
real(dp), parameter :: longitude     = longitude_deg * PI/180.0d0  ! [rad]

real(dp), parameter :: fcor = 2*Omega*sin(latitude)  ! Coriolis parameter at Hyltemossa

!-----------------------------------------------------------------------------------------
! Grid parameters
!-----------------------------------------------------------------------------------------
integer, parameter :: nz = 50  ! [-], number of height levels

! Model height levels, [m]
real(dp), parameter, dimension(nz) :: &
  hh = (/    0,   10,   20,   30,   40,   50,   60,   70,   80,   90, &
           100,  120,  140,  160,  180,  200,  230,  260,  300,  350, &
           400,  450,  500,  550,  600,  650,  700,  800,  900, 1000, &
          1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, &
          2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000 /)

real(dp), parameter :: hc = 10.0_dp  ! [m], canopy height
integer :: hh_index   ! loop index for the altitude array

!-----------------------------------------------------------------------------------------
! Time variables
!-----------------------------------------------------------------------------------------
integer, parameter :: one_hour = 60*60  ! [s], one hour in seconds

real(dp) :: time                  ! [s], current time
real(dp) :: time_start, time_end  ! [s], start and end time

real(dp) :: dt         ! [s], time step for main loop, usually is equal to meteorology time step
real(dp) :: dt_emis    ! [s], time step for emission calculation
real(dp) :: dt_chem    ! [s], time step for chemistry calculation
real(dp) :: dt_depo    ! [s], time step for deposition calculation
real(dp) :: dt_aero    ! [s], time step for aerosol calculation
real(dp) :: dt_output  ! [s], time step for output

real(dp) :: time_start_emission    ! [s], time to start calculating emission
real(dp) :: time_start_chemistry   ! [s], time to start calculating chemistry
real(dp) :: time_start_deposition  ! [s], time to start calculating deposition
real(dp) :: time_start_aerosol     ! [s], time to start calculating aerosol

integer :: daynumber_start  ! [day], start day of year
integer :: daynumber        ! [day], current day of year

integer :: counter  ! [-], counter of time steps

!-----------------------------------------------------------------------------------------
! Meteorology variables
!-----------------------------------------------------------------------------------------
real(dp), dimension(nz  ) :: uwind, &     ! [m s-1], u component of wind
                             vwind, &     ! [m s-1], v component of wind
                             theta        ! [K], potential temperature
real(dp), dimension(nz  ) :: uwind_new, &     ! [m s-1], u component of wind
                             vwind_new, &     ! [m s-1], v component of wind
                             theta_new        ! [K], potential temperature    
                             
real(dp), dimension(nz  ) :: temp, &   ! [K], air temperature
                             pres      ! [Pa], air pressure
                
real(dp), dimension(nz-1) :: K_m       ! [m^2/s], turbulent diffusion coefficient
real(dp), dimension(nz-1) :: K_h       ! [m^2/s], turbulent diffusion coefficient
real(dp), dimension(nz-1) :: Ri_a      ! array with Richardson nr-s, for testing

!-----------------------------------------------------------------------------------------
! Emission variables
!-----------------------------------------------------------------------------------------
real(dp), dimension(nz-1) :: F_veg_isoprene, &     ! Isoprene emission rate
                             F_veg_monoterpene     ! Monoterpene emission rate
real(dp) :: exp_coszen    ! solar radiation

integer :: i, j  ! used for loops

!-----------------------------------------------------------------------------------------
! Chemistry variables
!-----------------------------------------------------------------------------------------
real(dp), dimension(neq, nz) :: conc, dconsdt
real(dp), dimension(neq, nz) :: conc_new         ! [molecules / cm3], number concentration 
real(dp), dimension(nz) :: O2, N2, H2O, M

!-----------------------------------------------------------------------------------------
! Aerosol variables
!-----------------------------------------------------------------------------------------
real(dp), dimension(2, nz) :: CS
real(dp), dimension(100, nz) :: particle_conc_hh, particle_conc_hh_new
real(dp), dimension(nz) :: PN_hh, PV_hh, PM_hh
integer, parameter :: nr_bins=100 

!-----------------------------------------------------------------------------------------
! Deposition variables (local to main loop scope)
!-----------------------------------------------------------------------------------------
real(dp) :: wind_speed10m         ! Calculated wind speed at 10m for deposition call
real(dp) :: Richards_nr10m        ! Richardson number for deposition call
real(dp) :: DSWF                  ! Downward Shortwave Flux
real(dp) :: current_hourangle, current_zenith, current_coszen
real(dp), parameter :: solar_constant = 1361.0_dp ! [W/m2], extraterrestrial solar flux

!-----------------------------------------------------------------------------------------
! Initialization
!-----------------------------------------------------------------------------------------

call time_init()                 ! initialize time
call meteorology_init()          ! initialize meteorology
! initialize isoprene and monoterpene emissions
F_veg_isoprene      = 0.0_dp 
F_veg_monoterpene   = 0.0_dp
! Initialize aerosol properties
call aerosol_init(diameter, particle_mass, particle_volume, particle_conc, & 
                          particle_density, nucleation_coef, molecular_mass, molar_mass, & 
                          molecular_volume, molecular_dia, mass_accomm)
do hh_index=1, nz
  particle_conc_hh(:, hh_index) = particle_conc(:)
end do

call open_files()        ! open output files
call write_files(time)   ! write initial values

!-----------------------------------------------------------------------------------------
! Start main loop
!-----------------------------------------------------------------------------------------

DO WHILE (time <= time_end)
  !---------------------------------------------------------------------------------------
  ! Meteorology
  !---------------------------------------------------------------------------------------
  ! Compute K_m for the current time step based on current wind profiles
  call get_K(model_v, hh, uwind, vwind, theta, K_m, K_h, Ri_a)
  ! Set lower boundary condition
  call surface_values(theta(1), time+dt)

  ! Update meteorology
  DO hh_index = 2, size(hh) - 1
    ! Update uwind
    uwind_new(hh_index) = uwind(hh_index) + dt * ( &
                     fcor * (vwind(hh_index) - vg) + &
                     (K_m(hh_index) * (uwind(hh_index+1) - uwind(hh_index)) / (hh(hh_index+1) - hh(hh_index)) - &
                     K_m(hh_index-1) * (uwind(hh_index) - uwind(hh_index-1)) / (hh(hh_index) - hh(hh_index-1))) / &
                     ((hh(hh_index+1) - hh(hh_index-1)) / 2.0_dp))
  END DO

  DO hh_index = 2, size(hh) - 1
    ! Update vwind
    vwind_new(hh_index) = vwind(hh_index) + dt * ( &
                     -fcor * (uwind(hh_index) - ug) + &
                     (K_m(hh_index) * (vwind(hh_index+1) - vwind(hh_index)) / (hh(hh_index+1) - hh(hh_index)) - &
                     K_m(hh_index-1) * (vwind(hh_index) - vwind(hh_index-1)) / (hh(hh_index) - hh(hh_index-1))) / &
                     ((hh(hh_index+1) - hh(hh_index-1)) / 2.0_dp))
  END DO
  
  DO hh_index = 2, size(hh) - 1
    ! Update potent. temperature
    theta_new(hh_index) = theta(hh_index) + dt * ( &
                     K_h(hh_index) * (theta(hh_index+1) - theta(hh_index)) / (hh(hh_index+1) - hh(hh_index)) - &
                     K_h(hh_index-1) * (theta(hh_index) - theta(hh_index-1)) / (hh(hh_index) - hh(hh_index-1))) / &
                     ((hh(hh_index+1) - hh(hh_index-1)) / 2.0_dp)                 
  END DO
  ! Update uwind, vwind and theta arrays with new meteorological state
  uwind(2:nz-1) = uwind_new(2:nz-1)
  vwind(2:nz-1) = vwind_new(2:nz-1)
  theta(2:nz-1) = theta_new(2:nz-1)
  
  temp = theta - (grav/Cp)*hh
  pres = barometric_law(p00, temp, hh)
  !---------------------------------------------------------------------------------------
  ! Emission
  !---------------------------------------------------------------------------------------
  ! Start to calculate emission after time_start_emission
  ! Compute emission part every dt_emis, multiplying 1000 to convert s to ms to make mod easier
  if ( use_emission .and. time >= time_start_emission ) then
    if ( mod( nint((time - time_start_emission)*1000.0d0), nint(dt_emis*1000.0d0) ) == 0 ) then
      exp_coszen = get_exp_coszen(time, daynumber, latitude)
      ! Calculate emission rates
      call get_emissions(exp_coszen, temp(2), F_veg_isoprene(2), F_veg_monoterpene(2))  
      ! Update concentration for isoprene
      conc(13,2) = conc(13,2) + (F_veg_isoprene(2) * dt_emis) / (hc*100)
      ! Update concentration for monoterpenes
      conc(23,2) = conc(23,2) + (F_veg_monoterpene(2) * dt_emis) / (hc*100)
    end if
  end if

  if ( use_emission .and. (.not. use_chemistry) ) then
    ! Add emission to the number concentrations of compounds
    ! Convert emissions from flux (molecules/cm2/s) to number concentration (molecules/cm3)
    ! Update concentration for isoprene
    ! conc(13,2) = conc(13,2) + (F_veg_isoprene(2) * dt_emis) / (hc*100)
    ! Update concentration for monoterpenes
    ! conc(23,2) = conc(23,2) + (F_veg_monoterpene(2) * dt_emis) / (hc*100)
  end if

  !---------------------------------------------------------------------------------------
  ! Deposition
  !---------------------------------------------------------------------------------------
  ! Start to calculate gas dry deposition velocity after time_start_deposition
  ! Compute deposition part every dt_depo, multiplying 1000 to convert s to ms to make mod easier
  if ( use_deposition .and. time >= time_start_deposition ) then
    if ( mod( nint((time - time_start_deposition)*1000.0d0), nint(dt_depo*1000.0d0) ) == 0 ) then

      ! Wind speed magnitude at level 2 (10m)
      wind_speed10m = sqrt(uwind(2)**2 + vwind(2)**2)

      ! Richardson number at level 2 (10m)
      if (model_v == 3) then
         Richards_nr10m = Ri_a(2)
      else
         ! if Ri not calculated
         Richards_nr10m = 0.0_dp 
      end if

      ! Calculate Downward Shortwave Flux (DSWF)
      exp_coszen = get_exp_coszen(time, daynumber, latitude)
      DSWF = 486.66_dp * exp_coszen ! [W m-2]

      ! Calculate deposition velocity for particles and gases
      call dry_dep_velocity(temp(2), pres(2), DSWF, Richards_nr10m, wind_speed10m, vd_gas, vd_particle)

      if (use_aerosol) then
        do i = 1, nr_bins
          ! Update particle concentrations by removing deposited particles at level 2 which includes canopy and soil
          particle_conc_hh(i, 2) = particle_conc_hh(i, 2) * exp(-vd_particle(i) / hh(2) * dt_depo)
        end do
      end if
      
      ! Update gas concentrations by removing deposited gases at level 2
      conc(20, 2) = conc(20, 2) * exp(-vd_gas(1) / hh(2) * dt_depo)  ! SO2
      conc( 1, 2) = conc( 1, 2) * exp(-vd_gas(2) / hh(2) * dt_depo)  ! O3
      conc(17, 2) = conc(17, 2) * exp(-vd_gas(3) / hh(2) * dt_depo)  ! HNO3
      conc(13, 2) = conc(13, 2) * exp(-vd_gas(4) / hh(2) * dt_depo)  ! isoprene
      conc(23, 2) = conc(23, 2) * exp(-vd_gas(5) / hh(2) * dt_depo)  ! apinene
    end if
  end if

  !---------------------------------------------------------------------------------------
  ! Chemistry
  !---------------------------------------------------------------------------------------
  ! Start to calculate chemical reactions only after some time to save the computation time
  ! Compute chemistry part every dt_chem, multiplying 1000 to convert s to ms to make mod easier
  if ( use_chemistry .and. time >= time_start_chemistry ) then
    if ( mod( nint((time - time_start_chemistry)*1000.0d0), nint(dt_chem*1000.0d0) ) == 0 ) then
      ! Solve chemical equations for each layer except boundaries
      exp_coszen = get_exp_coszen(time, daynumber, latitude)
      do hh_index=2, nz-1

        M(hh_index)    = pres(hh_index)*NA / (Rgas*temp(hh_index)) * 1d-6   ! Air molecules concentration [molecules/cm3]
        O2(hh_index)   = 0.21d0*M(hh_index)                                 ! Oxygen
        N2(hh_index)   = 0.78d0*M(hh_index)                                 ! Nitrogen
        H2O(hh_index)  = 1.0D16                                             ! Water
        conc( 1, hh_index) = 40.0d0   * M(hh_index) * ppb     ! O3
        conc( 5, hh_index) = 0.2d0    * M(hh_index) * ppb     ! NO2
        conc( 6, hh_index) = 0.07d0   * M(hh_index) * ppb     ! NO
        conc( 9, hh_index) = 200.0d0  * M(hh_index) * ppb     ! CO
        conc(11, hh_index) = 1759.0d0 * M(hh_index) * ppb     ! CH4
        conc(20, hh_index) = 2.0d0    * M(hh_index) * ppb     ! SO2

        ! CS(1, hh_index) = 0.001_dp  ! CS for H2SO4
        ! CS(2, hh_index) = 0.001_dp  ! CS for ELVOC
        call chemistry_step(conc(1:neq, hh_index), time, time+dt_chem            , &
                           O2(hh_index), N2(hh_index), M(hh_index), H2O(hh_index), &
                           temp(hh_index), exp_coszen                            , &
                           F_veg_isoprene(hh_index), F_veg_monoterpene(hh_index) , &
                           CS(1, hh_index), CS(2, hh_index)) 
      end do
    end if  ! every dt_chem
  end if

  ! Update concentrations of gas phase compounds if any of these processes are considered
  ! Deposition should not be used alone because it calculates nothing in that case
  if (use_emission .or. use_chemistry) then
    ! Trick to make bottom flux zero
    conc(1:neq,1) = conc(1:neq,2) ! concentration for layer 1 and layer 2 equal => no flux
    conc(1:neq,nz) = 0.0_dp       ! concentration = 0 at the top layer
    ! Concentrations can not be lower than 0
    ! Mixing of chemical species
    do i=1, neq
        do hh_index = 2, size(hh) - 1
          conc_new(i, hh_index) = conc(i, hh_index) + dt * ( &
          K_h(hh_index) * (conc(i, hh_index+1) - conc(i, hh_index)) / (hh(hh_index+1) - hh(hh_index)) - &
          K_h(hh_index-1) * (conc(i, hh_index) - conc(i, hh_index-1)) / (hh(hh_index) - hh(hh_index-1))) / &
          ((hh(hh_index+1) - hh(hh_index-1)) / 2.0_dp)                 
        end do
    end do
    conc = conc_new
    ! Set the constraints above again for output
    conc(1:neq,1) = conc(1:neq,2) ! concentration for layer 1 and layer 2 equal => no flux
  end if

  !---------------------------------------------------------------------------------------
  ! Aerosol
  !---------------------------------------------------------------------------------------
  ! Start to calculate aerosol processes only after some time to save the computation time
  ! Compute aerosol part every dt_aero, multiplying 1000 to convert s to ms to make mod easier
  if ( use_aerosol .and. time >= time_start_aerosol ) then
    if ( mod( nint((time - time_start_aerosol)*1000.0d0), nint(dt_aero*1000.0d0) ) == 0 ) then
      ! Nucleation, condensation, coagulation and deposition of particles
      do hh_index=2, nz-1
        ! Initialize particle_conc for this height level from the last timestep
        particle_conc(:) = particle_conc_hh(:, hh_index) 
        ! H2SO4 and ELVOC concentrations at this height level
        cond_vapour(1) = conc(21, hh_index) * 10.0_dp**6.0_dp ! [molec/cm3] 
        cond_vapour(2) = conc(25, hh_index) * 10.0_dp**6.0_dp ! [molec/cm3] 

        ! Compute nucleation with H2SO4
        call nucleation(dt_aero, cond_vapour(1), nucleation_coef, particle_conc)

        ! Compute condensation (updates CS for H2SO4 and ELVOC)
        call condensation(dt_aero, temp(hh_index), pres(hh_index), mass_accomm, molecular_mass, molecular_volume, &
                          molar_mass, molecular_dia, particle_mass, particle_volume, particle_conc, cond_sink,    &
                          diameter, cond_vapour)
  
        ! Compute coagulation
        call coagulation(dt_aero, particle_conc, diameter, temp(hh_index), pres(hh_index), particle_mass)

        ! Store Condensation Sink (CS) for H2SO4 and ELVOC at different altitudes
        CS(1, hh_index) = cond_sink(1)   ! CS for H2SO4
        CS(2, hh_index) = cond_sink(2)   ! CS for ELVOC

        ! Store particle concentration at different altitudes
        particle_conc_hh(:, hh_index) = particle_conc(:)
      end do
    end if  ! every dt_aero

    ! Trick to make bottom flux zero
    particle_conc_hh(1:nr_bins, 1) = particle_conc_hh(1:nr_bins, 2)
    ! Mixing of aerosol particles
    particle_conc_hh_new = 0.0_dp
    do hh_index=2, nz-1
      particle_conc_hh_new(:, hh_index) = particle_conc_hh(:, hh_index) + dt * ( &
      K_h(hh_index) * (particle_conc_hh(:, hh_index+1) - particle_conc_hh(:, hh_index)) / (hh(hh_index+1) - hh(hh_index)) - &
      K_h(hh_index-1) * (particle_conc_hh(:, hh_index) - particle_conc_hh(:, hh_index-1)) / (hh(hh_index) - hh(hh_index-1))) / &
      ((hh(hh_index+1) - hh(hh_index-1)) / 2.0_dp)                 
    end do
    particle_conc_hh(:, 2:nz-1) = particle_conc_hh_new(:, 2:nz-1)

    ! Trick to make bottom flux zero
    particle_conc_hh(1:nr_bins, 1) = particle_conc_hh(1:nr_bins, 2)

    ! Update particle nr, particle mass, particle volume data for output files
    do hh_index = 1, nz
      PN_hh(hh_index) = sum(particle_conc_hh(:, hh_index)) * 1D-6  ! [cm-3]
      PM_hh(hh_index) = sum(particle_conc_hh(:, hh_index) * particle_mass) * 1D9    ! [μg/m3]
      PV_hh(hh_index) = sum(particle_conc_hh(:, hh_index) * particle_volume) * 1D12 ! [μm3/cm3]
    end do

  end if

  !---------------------------------------------------------------------------------------
  ! Ending loop actions
  !---------------------------------------------------------------------------------------
  ! Advance to next time step
  time = time + dt
  if ( mod( nint((time - time_start)*1000.0d0), nint(24*3600*1000.0d0) ) == 0) then
    daynumber = daynumber + 1
  end if

  ! Write data every dt_output [s]
  if ( mod( nint((time - time_start)*1000.0d0), nint(dt_output*1000.0d0) ) == 0 ) then
    write(*, '(a8,f8.3,a8)') 'time = ', time/one_hour, '   hours'
    call write_files(time)
  end if

  ! Count loop number
  counter = counter + 1

end do
!-----------------------------------------------------------------------------------------
! Finalization
!-----------------------------------------------------------------------------------------
! Close all the opened files
call close_files()

! Count total time steps
write(*,*) counter,'time steps'


contains

!-----------------------------------------------------------------------------------------
! subroutine open_files()
!
! Open needed files
!-----------------------------------------------------------------------------------------
subroutine open_files()
  logical :: dir_exist

  ! Create a new directory if it does not exist
  inquire(file=trim(adjustl(output_dir)), exist=dir_exist)
  if (.not. dir_exist) then
    ! This line may change for different operating systems
    call system('mkdir ' // trim(adjustl(output_dir)))
  end if

  ! Open files to write output results
  open( 8,file=trim(adjustl(output_dir))//'/time.dat' ,status='replace',action='write')
  open( 9,file=trim(adjustl(output_dir))//'/hh.dat'   ,status='replace',action='write')
  open(10,file=trim(adjustl(output_dir))//'/uwind.dat',status='replace',action='write')
  open(11,file=trim(adjustl(output_dir))//'/vwind.dat',status='replace',action='write')
  open(12,file=trim(adjustl(output_dir))//'/theta.dat',status='replace',action='write')
  open(13,file=trim(adjustl(output_dir))//'/Km.dat'   ,status='replace',action='write')
  open(14,file=trim(adjustl(output_dir))//'/Kh.dat'   ,status='replace',action='write')
  open(15,file=trim(adjustl(output_dir))//'/Ri.dat'   ,status='replace',action='write')
  open(16,file=trim(adjustl(output_dir))//'/Emissions.dat'   ,status='replace',action='write')
  open(17,file=trim(adjustl(output_dir))//'/Concentrations_h10.dat', status='replace',action='write')
  open(18,file=trim(adjustl(output_dir))//'/Concentrations_h50.dat', status='replace',action='write')
  open(19,file=trim(adjustl(output_dir))//'/Concentrations_h500.dat', status='replace',action='write')
  open(20,file=trim(adjustl(output_dir))//'/Concentrations_h2000.dat', status='replace',action='write')
  open(21,file=trim(adjustl(output_dir))//'/PN.dat', status='replace',action='write')
  open(22,file=trim(adjustl(output_dir))//'/PV.dat', status='replace',action='write')
  open(23,file=trim(adjustl(output_dir))//'/PM.dat', status='replace',action='write')
  open(24,file=trim(adjustl(output_dir))//'/particle_conc_100.dat', status='replace',action='write')
  open(25,file=trim(adjustl(output_dir))//'/particle_conc_500.dat', status='replace',action='write')
  open(26,file=trim(adjustl(output_dir))//'/dep_v_gas.dat', status='replace',action='write')
  open(27,file=trim(adjustl(output_dir))//'/dep_v_particle.dat', status='replace',action='write')
end subroutine open_files


!-----------------------------------------------------------------------------------------
! subroutine write_files(time)
!
! Write data to files at time
!-----------------------------------------------------------------------------------------
subroutine write_files(time)
  real(dp) :: time  ! current time
  character(255) :: outfmt_one_scalar, outfmt_two_scalar, outfmt_level, outfmt_mid_level, outfmt_level_bins, outfmt_level_species

  ! Output real data with scientific notation with 16 decimal digits
  outfmt_one_scalar = '(es25.16e3)'                               ! for scalar
  write(outfmt_level     , '(a, i3, a)') '(', nz  , 'es25.16e3)'  ! for original levels
  write(outfmt_mid_level , '(a, i3, a)') '(', nz-1, 'es25.16e3)'  ! for middle levels
  write(outfmt_two_scalar, '(a, i3, a)') '(', 2   , 'es25.16e3)'  ! for two scalars
  write(outfmt_level_bins, '(a, i3, a)') '(', nr_bins  , 'es25.16e3)'  ! for first level with aerosol
  write(outfmt_level_species, '(a, i3, a)') '(', neq , 'es25.16e3)' ! for all species all altitude levels


  ! Only output hh once
  if (time == time_start) then
    write(9, outfmt_level) hh
  end if

  ! Output every output time step
  write( 8, outfmt_one_scalar) time/(24*one_hour)  ! [day]
  write(10, outfmt_level     ) uwind
  write(11, outfmt_level     ) vwind
  write(12, outfmt_level     ) theta
  write(13, outfmt_level     ) K_m
  write(14, outfmt_level     ) K_h
  write(15, outfmt_level     ) Ri_a
  write(16, *                ) F_veg_isoprene(2), F_veg_monoterpene(2)
  write(17, outfmt_level     ) conc(:,6)
  write(18, outfmt_level     ) conc(:,6)
  write(19, outfmt_level     ) conc(:,23)
  write(20, outfmt_level     ) conc(:,40)
  write(21, outfmt_level     ) PN_hh
  write(22, outfmt_level     ) PV_hh
  write(23, outfmt_level     ) PM_hh
  write(24, outfmt_level_bins) particle_conc_hh(:,11) ! 100 m
  write(25, outfmt_level_bins) particle_conc_hh(:,23) ! 500 m
  write(26, outfmt_level     ) vd_gas
  write(27, outfmt_level_bins) vd_particle

end subroutine write_files


!-----------------------------------------------------------------------------------------
! subroutine Close_Files()
!
! Close files
!-----------------------------------------------------------------------------------------
subroutine close_files()
  close(8)
  close(9)
  close(10)
  close(11)
  close(12)
  close(13)
  close(14)
  close(15)
  close(16)
  close(17)
  close(18)
  close(19)
  close(20)
  close(21)
  close(22)
  close(23)
  close(24)
  close(25)
  close(26)
  close(27)
end subroutine close_files


!-----------------------------------------------------------------------------------------
! subroutine time_init()
!
! Time initiation
!-----------------------------------------------------------------------------------------
subroutine time_init()
  ! Basic time variables
  time_start = 0.0d0
  time_end   = 5.0d0 * 24.0d0 * one_hour
  time       = time_start

  ! Time steps
  dt        = 0.5d0
  dt_emis   = 0.5d0
  dt_chem   = 10.0d0
  dt_depo   = 10.0d0
  dt_aero   = 10.0d0
  dt_output = 3600.0d0

  ! Day number
  daynumber_start = 31+28+31+6  ! day is April 6th, 2018
  daynumber       = daynumber_start

  ! Start time for each process
  time_start_chemistry  = 3.0 * 24.0 * one_hour
  time_start_deposition = 3.0 * 24.0 * one_hour
  time_start_emission   = 4.625d0 * 24d0 * one_hour   ! emission starts at 4.625 days
  time_start_aerosol    = 4.0 * 24.0 * one_hour     ! aerosol starts at 4.0 days

  ! Loop number
  counter = 0
end subroutine time_init


!-----------------------------------------------------------------------------------------
! subroutine meteorology_init()
!
! Meteorology initiation
!-----------------------------------------------------------------------------------------
subroutine meteorology_init()
  ! Wind velocity
  uwind         = 0.0d0
  uwind(nz)     = ug
  uwind(2:nz-1) = uwind(nz) * hh(2:nz-1)/hh(nz)

  vwind = 0.0d0
  vwind(nz) = vg

  ! Potential temperature
  theta     = 273.15d0 + 0.0d0
  theta(nz) = 273.15d0 + 5.0d0

  ! Air temperature and pressure
  temp = theta - (grav/Cp)*hh
  pres = barometric_law(p00, temp, hh)
end subroutine meteorology_init


!-----------------------------------------------------------------------------------------
! Get the surface values from the input data file
! Now only the temperature is used.
!-----------------------------------------------------------------------------------------
subroutine surface_values(temperature, time)

  ! (Note: can also get water concentrantion, in ppt, if modify this
  ! subroutine to also use column 8)
  !
  ! Data is taken from:
  ! http://avaa.tdata.fi/web/smart

  real(dp), intent(in)            :: time ! input, in seconds
  real(dp), intent(out)           :: temperature ! output, in Kelvin
  logical, save                   :: first_time = .true.
  real(dp), dimension(8,50), save :: surface_data ! summer
  real(dp), dimension(50), save   :: temperature_data
  real(dp), parameter             :: seconds_in_day = 24*60*60
  real(dp), parameter             :: seconds_in_30min = 30*60
  integer                         :: index
  real(dp) :: time24h, time30min, time24plus15, temp1, temp2, x

  ! Only when called for the first time, read in data from file
  ! With this trick, we don't need to open the file in the main program
  if (first_time) then
     open(30, file=trim(adjustl(input_dir))//'/hyltemossa_2018_4_06_t_h2o.dat', status='old')
     read(30, *) surface_data
     temperature_data(1:50) = surface_data(7,1:50) ! in Celcius
     first_time = .false.
  end if

  time24h = modulo(time, seconds_in_day) ! time modulo 24 hours
  time24plus15 = time24h + 15*60 ! time since 23:45 previous day
  time30min = modulo(time24plus15, seconds_in_30min)
  index = 1 + floor(time24plus15/seconds_in_30min)

  temp1 = temperature_data(index)
  temp2 = temperature_data(index + 1)
  x = time30min/seconds_in_30min

  ! linear interpolation between previous and next temperature data value
  temperature = temp1 + x*(temp2 - temp1) + 273.15_dp ! now in Kelvin


end subroutine surface_values


!-----------------------------------------------------------------------------------------
! Get K (turbulent	diffusivity)
!-----------------------------------------------------------------------------------------
subroutine get_K(model_v, hh, uwind, vwind, theta, K_m, K_h, Ri_a)
! inputs
real(dp), dimension(nz), intent(in)  :: hh
real(dp), dimension(nz), intent(in)  :: uwind, vwind, theta
integer, intent(in)                  :: model_v
! output
real(dp), dimension(nz-1), intent(out) :: K_m, K_h  ! turbulent diffusion coefficient array [m^2/s]
real(dp), dimension(nz-1), intent(out) :: Ri_a  ! array of Richardson nr for testing the meteorology 
! constants
real(dp), parameter                  :: k = 0.4_dp  ! von Kármán constant
real(dp), parameter                  :: lambda = 300.0_dp    ! mixing length scale [m]
real(dp), parameter                  :: grav = 9.81_dp    ! [m s-2], gravitation
! local variables
integer                              :: hh_index
real(dp)                             :: L   ! Blackadar mixing length
real(dp)                             :: du_dz, dv_dz, windshear
real(dp)                             :: Ri    ! Richardson nr
real(dp)                             :: f_m, f_h  ! Dyer-Businger forms
real(dp)                             :: a1, denom

! Model version 1
IF (model_v == 1) THEN
  K_m = 5.0_dp ! [m^2/s]
  K_h = 5.0_dp ! [m^2/s]

! Model version 2
ELSE IF (model_v == 2) THEN
  ! Calculate K_m for every altitude, except for boundary conditions
  DO hh_index = 1, size(hh) - 1
    ! Compute mixing length l
    
    ! L = k * hh(hh_index) / (1.0_dp + (k * hh(hh_index) / lambda))
    ! eddies are also at model midpoint levels 
    L = k * (hh(hh_index+1)+hh(hh_index))*0.5d0 / (1.0_dp + (k * (hh(hh_index+1)+hh(hh_index))*0.5d0 / lambda))
    ! Calculate velocity changes with altitude
    du_dz = (uwind(hh_index+1) - uwind(hh_index)) / (hh(hh_index+1) - hh(hh_index))
    dv_dz = (vwind(hh_index+1) - vwind(hh_index)) / (hh(hh_index+1) - hh(hh_index))
    ! Calculate windshear and K_m
    windshear = sqrt((du_dz**2.0_dp) + (dv_dz**2.0_dp))
    K_m(hh_index) = L**2.0_dp * windshear
  END DO
  K_h = K_m

!Model version 3
ELSE IF (model_v == 3) THEN
  ! calculate K_m at every altitude for uwind and vwind and K_h for theta
  DO hh_index = 1, size(hh) - 1
    ! calculate Richardson nr
    denom = ((uwind(hh_index+1) - uwind(hh_index))**2.0_dp + &
            (vwind(hh_index+1)  - vwind(hh_index))**2.0_dp)
    Ri = grav / ((theta(hh_index+1) + theta(hh_index)) / 2.0_dp)  *  &
                ((theta(hh_index+1) - theta(hh_index)) / denom)   *  &
                (hh(hh_index+1) - hh(hh_index))
    ! Fix Richardson number to reasonable bounds to avoid extremly low values
    ! IF (Ri < -1.5_dp) THEN
    !   Ri = -1.5_dp
    ! END IF
    
    ! calculate Dyer-Businger form
    ! unstable conditions
    IF (Ri < 0.0_dp) THEN
      f_m = (1.0_dp - 16.0_dp*Ri)**(0.5_dp)
      f_h = (1.0_dp - 16.0_dp*Ri)**(0.75_dp)
    ! conditions?
    ELSE IF (Ri >= 0.0_dp .AND. Ri < 0.2_dp) THEN
      a1  = (1.0_dp - 5.0_dp*Ri)**2.0_dp
      f_m = max(a1, 0.1_dp)
      f_h = max(a1, 0.1_dp)
    ! very stable conditions
    ELSE IF (Ri >= 0.2_dp) THEN
      f_m = 0.1_dp
      f_h = 0.1_dp
 
    END IF

    ! Compute mixing length l
    L = k * (hh(hh_index+1)+hh(hh_index))*0.5d0 / (1.0_dp + (k * (hh(hh_index+1)+hh(hh_index))*0.5d0 / lambda))
    ! Calculate velocity changes with altitude
    du_dz = (uwind(hh_index+1) - uwind(hh_index)) / (hh(hh_index+1) - hh(hh_index))
    dv_dz = (vwind(hh_index+1) - vwind(hh_index)) / (hh(hh_index+1) - hh(hh_index))
    ! Calculate windshear
    windshear = sqrt(MAX(0.0_dp, (du_dz**2.0_dp) + (dv_dz**2.0_dp)))
    ! calculate K_m and K_h
    K_m(hh_index) = (L**2.0_dp) * windshear * f_m
    K_h(hh_index) = (L**2.0_dp) * windshear * f_h
    ! append Richardson nr to an array
    Ri_a(hh_index) = Ri

  END DO
END IF

end subroutine get_K

!-----------------------------------------------------------------------------------------
! Get emissions
!-----------------------------------------------------------------------------------------
subroutine get_emissions(exp_coszen, temp, F_veg_isoprene, F_veg_monoterpene)

real(dp), intent(in)                 :: exp_coszen, temp
real(dp), intent(out)                :: F_veg_isoprene, &     ! Surface emission flux for isoprene
                                        F_veg_monoterpene     ! Surface emission flux for isoprene
real(dp)                             :: gamma_isoprene,    &  ! adjustment factor dependent on T and light emission activity
                                        gamma_monoterpene, &  ! adjustment factor dependent on T and light emission activity 
                                        C_L,               &  
                                        C_T,               &
                                        PAR            
real(dp), parameter                  :: D_m = 0.0538_dp,    & ! Foliar density [g cm^-2]
                                        eeta = 100.0_dp,    & ! ecosystem dependent emission factor [ng g^-1 h^-1]
                                        delta = 1.0_dp,     & ! emission activity factor for long term controls
                                        alpha = 0.0027_dp,  & ! 
                                        c_L1 = 1.006_dp,    &
                                        c_T1 = 95.0e3_dp,     & ! [kJ mol^-1]
                                        c_T2 = 230.0e3_dp,    & ! [kJ mol^-1]
                                        T_s = 303.15_dp,    & ! [K]
                                        T_m = 314.0_dp,     & ! [K]
                                        beeta = 0.09_dp       ! K^-1
real(dp), parameter                  :: M_isoprene = 68.12_dp, &  ! g/mol
                                        M_monoterpene = 136.23_dp  ! g/mol
real(dp)                             :: height = 1000.0_dp  ! height (cm)
           
PAR = 1000.0_dp * exp_coszen
C_L = alpha * c_L1 * PAR / sqrt(1.0_dp + alpha**2.0_dp * PAR**2.0_dp)
C_T = exp(c_T1 * (temp - T_s) / (Rgas * temp * T_s)) / (1.0_dp + exp(c_T2*(temp - T_m)/ (Rgas*temp*T_s)))

! isoprene emissions at 5-15m
gamma_isoprene = C_L * C_T
F_veg_isoprene = D_m * eeta * gamma_isoprene * delta

! monoterpene emissions at 5-15m
gamma_monoterpene = exp(beeta * (temp - T_s))
F_veg_monoterpene = D_m * eeta * gamma_monoterpene * delta

! Make sure F_veg is in correct units
! Convert from ng cm**-2 h**-1 to ng cm**-2 s⁻¹
F_veg_isoprene = F_veg_isoprene / 3600.0_dp
F_veg_monoterpene = F_veg_monoterpene / 3600.0_dp
! Convert ng to molecules
F_veg_isoprene = F_veg_isoprene * (1.0_dp / 10.0_dp**9) * (1.0_dp / M_isoprene) * NA
F_veg_monoterpene = F_veg_monoterpene * (1.0_dp / 10.0_dp**9) * (1.0_dp / M_monoterpene) * NA
! Convert from molecules per cm² per s to molecules per cm³ per s
F_veg_isoprene = F_veg_isoprene / height 
F_veg_monoterpene = F_veg_monoterpene / height

end subroutine get_emissions



!-----------------------------------------------------------------------------------------
! Calculate the radiation related quantities
!-----------------------------------------------------------------------------------------
real(dp) function get_exp_coszen(time,daynumber,latitude)
  real(dp), intent(in) :: time,latitude
  INTEGER, intent(in) :: daynumber
  real(dp) :: hourangle,zenith,coszen
  hourangle = get_hourangle(time)
  zenith = solar_zenith_angle(hourangle,daynumber,latitude)
  coszen = cos(zenith)
  IF (coszen > 0) THEN  ! sun is above horizon
     get_exp_coszen = exp(-0.575_dp/coszen)
  ELSE
     get_exp_coszen = 0.0_dp
  endIF
end function get_exp_coszen


real(dp) function get_hourangle(time)
  real(dp), intent(in) :: time
  real(dp), parameter :: one_day = 24*one_hour
  get_hourangle = modulo(time,one_day)/one_day * 2 * pi - pi
end function get_hourangle


real(dp) function solar_zenith_angle(hourangle,daynumber,latitude)
  ! http://en.wikipedia.org/wiki/Solar_elevation_angle
  ! http://en.wikipedia.org/wiki/Position_of_the_Sun
  INTEGER, intent(in) :: daynumber
  real(dp), intent(in) :: hourangle,latitude
  real(dp) :: declination,elevation
  real(dp), parameter :: to_rad = pi/180.0_dp

  declination = -23.44_dp * to_rad * cos(2 * pi * (daynumber + 10)/365.0_dp)
  elevation = cos(hourangle)*cos(declination)*cos(latitude) &
       + sin(declination)*sin(latitude)
  solar_zenith_angle = pi/2.0_dp - elevation
  ! Notes:
  ! - Not tested near equador or on the southern hemisphere.
  ! - solar_zenith_angle can be larger than pi/2, it just means
  !   the sun is below horizon.
  ! - solar_zenith_angle assumes time is in local solar time, which
  !   is usually not exactly true
end function solar_zenith_angle


!-----------------------------------------------------------------------------------------
! Other functions
!-----------------------------------------------------------------------------------------
function barometric_law(p00, tempK, h) result(p)
  real(dp), intent(in) :: p00, tempK(nz), h(nz)
  real(dp) :: p(nz)
  real(dp) :: dh(nz)

  dh(2:nz) = h(2:nz) - h(1:nz-1)

  p(1) = p00
  do i=2, nz
    p(i) = p(i-1)*exp(-mm_air*grav/(Rgas*(tempK(i-1)+tempK(i))/2.0d0)*dh(i))
  end do
end function barometric_law

end program main
