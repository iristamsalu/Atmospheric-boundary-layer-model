MODULE aerosol_mod

IMPLICIT NONE

PRIVATE

PUBLIC :: pi
PUBLIC :: dp, cond_vapour, diameter, particle_mass, particle_volume, particle_conc, &
          particle_density, nucleation_coef, molecular_mass, molar_mass, &
          molecular_volume, molecular_dia, mass_accomm, &
          PN, PM, nucleation_rate, cond_sink, particle_volume_conc
PUBLIC :: aerosol_init, nucleation, condensation, coagulation, dry_dep_velocity
! Dry deposition variables
PUBLIC :: vd_particle, vd_gas


!====================== Definition of variables =====================================================================!
INTEGER, PARAMETER :: dp = SELECTED_REAL_KIND(15,300)
! so that numbers will be in 64bit floating point
! http://en.wikipedia.org/wiki/Double_precision_floating-point_format

REAL(dp), PARAMETER :: pi   = 2D0*ASIN(1D0)  ! constant pi
REAL(dp), PARAMETER :: ka   = 0.4D0          ! [-], von Karman constant, dimensionless
REAL(dp), PARAMETER :: g    = 9.81D0         ! [m s-2], gravitation const
REAL(dp), PARAMETER :: Rg   = 8.3145D0       ! Universal gas constant J mol^-1 K^-1
REAL(dp), PARAMETER :: Na   = 6.022D23       ! Avogadro's number 
REAL(dp), PARAMETER :: Mair = 28.96D-3       ! Mean molecular weight of air
REAL(dp), PARAMETER :: kb   = 1.381d-23      ! Boltzmann constant [(m2*kg)/(s2*K)]

INTEGER, PARAMETER ::  nr_bins = 100           ! Number of particle size bins
INTEGER, PARAMETER ::  nr_cond = 2             ! Number of condensable vapours
  
REAL(dp), DIMENSION(nr_bins) :: diameter       , &  ! Diameter of each size bin
                                particle_mass  , &  ! mass of one particle in each size bin
                                particle_conc  , &  ! number concentration in each size bin
                                particle_volume, &  ! volume concentration in each size bin 
                                coag_loss      , &  ! coagulation loss rate of particles in each size bin
                                vd_particle         ! Dry deposition velocity of particles
     
REAL(dp), DIMENSION(nr_cond) :: molecular_mass  , &  ! molecular mass of the condensing vapours [kg/#]
                                molecular_volume, &  ! Molecule volume of condensable vapours [m^3]
                                molecular_dia   , &  ! Molecule diameter of condensable vapours [m]
                                molar_mass      , &  ! Molar mass of condensable vapours [kg/m^3]
                                cond_vapour          ! Concentration of condensable vapours [molec/m^3] 
                                      
REAL(dp), DIMENSION(nr_cond) :: cond_sink = 1.0d-3  ! Assumed initial condensation sink of vapours [s^-1]

REAL(dp) :: PN, PM  ! Total particle number [# m-3] and mass concentration [kg m-3]
     
REAL(dp) :: particle_density, &  ! [kg]
            nucleation_coef , &  ! Nucleation coefficient 
            mass_accomm          ! mass accomodation coefficient 

REAL(dp) :: nucleation_rate  ! [# m-3 s-1]

REAL(dp) :: particle_volume_conc  ! Particle volume concentration [μm³/cm³]

! Variables for gas deposition
INTEGER, PARAMETER :: num_gases=5
REAL(dp), DIMENSION(num_gases) :: vd_gas 


CONTAINS


SUBROUTINE aerosol_init(diameter, particle_mass, particle_volume, particle_conc, &
                        particle_density, nucleation_coef, molecular_mass, molar_mass, &
                        molecular_volume, molecular_dia, mass_accomm)

  !======================================!
  ! Definition of variables
  !======================================!

  REAL(dp), DIMENSION(nr_bins), INTENT(OUT) :: diameter       , &  ! [m], diamter of each size bin
                                               particle_mass  , &  ! [kg], mass of one particle
                                               particle_volume, &  ! [m3], volume of one particle
                                               particle_conc       ! [# m-3], number concentration
  
  REAL(dp), DIMENSION(nr_cond), INTENT(OUT) :: molecular_mass  , & ! [kg], molecular mass of the condensing vapours
                                               molecular_volume, & ! [m3]
                                               molecular_dia   , & ! [m]
                                               molar_mass          ! [kg mol-1], molar mass of the condensing vapours
  
  REAL(dp), INTENT(OUT) :: nucleation_coef, &  ! [m3 molec-1], nucleation coefficient
                           mass_accomm         ! [-], mass accomodation coefficient
  
  REAL(dp), DIMENSION(nr_cond) :: density  ! [kg m-3], Bulk density of condensing vapours
  
  REAL(dp) :: particle_density  ! [kg m-3], particle density
  
  INTEGER :: i

  nucleation_coef = 1D-21 ! [m3 molec-1 s-1]
  mass_accomm = 1D0
  
  !===== Particle properties =====!

  ! Particle diameters between 2D-9 and 2.5D-6 m:
  diameter(1)=2D-9 
  DO i=2,nr_bins
    diameter(i)=diameter(i-1)*(2.5D-6/diameter(1))**(1D0/(nr_bins-1))
  END DO
    
  particle_conc = 1D0 ! Assume an initial particle number concentration of 1 [# m-3]
  where((abs(diameter-2D-7)-MINVAL(abs(diameter-2D-7)))<1D-20)  particle_conc=2D8  ! add 200 [# cm-3] to 200 nm sized accumulation mode particles
  
  particle_density = 1.4D3                                       ! [kg m-3], assumed fixed particle density
  particle_volume = 1D0/6D0 * pi * diameter**3                   ! [m-3], single particle volume
  particle_mass=  1D0/6D0 * pi * diameter**3 * particle_density  ! [kg], single particle mass
  
  !===== Condensable vapor properties =====!

  density = (/1.84D3, 1.4D3/)                                ! density of sulphuric acid and ELVOC
  molar_mass = (/0.098D0, 0.3D0/)                            ! H2SO4 and ELVOC
  molecular_mass = molar_mass / Na                           ! molecular mass [kg]
  molecular_volume = molecular_mass / density                ! molecular volume [m-3]
  molecular_dia = (6D0 * molecular_volume / pi )**(1D0/3D0)  ! molecular diameter [m]

END SUBROUTINE aerosol_init
  
SUBROUTINE nucleation(timestep, cond_vapour, nucleation_coef, particle_conc)
  ! Consider how kinetic H2SO4 nucleation influence the number concentrations of particles 
  ! in the fist size bin particle_conc(1) within one model time step
  REAL(dp), INTENT(IN) :: nucleation_coef, & ! [m3 molec-1], nucleation coefficient
                          cond_vapour    , & ! [molec/m^3], concentration of condensable vapours 
                          timestep           ! [s]
  REAL(dp) :: nucleation_rate ! [# m-3 s-1], nucleation rate 
  REAL(dp), DIMENSION(nr_bins), INTENT(INOUT) :: particle_conc ! [# m-3], particle number concentration
  
  nucleation_rate = nucleation_coef * cond_vapour**2                ! [m-3 s-1]
  particle_conc(1) = particle_conc(1) + nucleation_rate * timestep  ! [# m-3]
END SUBROUTINE nucleation

SUBROUTINE condensation(timestep, temperature, pressure, mass_accomm, molecular_mass, &
                        molecular_volume, molar_mass, molecular_dia, particle_mass, particle_volume, &
                        particle_conc, cond_sink, diameter, cond_vapour)
  
  REAL(dp), DIMENSION(nr_bins), INTENT(IN) :: diameter, particle_mass
  REAL(dp), DIMENSION(nr_cond), INTENT(IN) :: molecular_mass, molecular_dia, &
                                              molecular_volume, molar_mass

  REAL(dp), DIMENSION(nr_cond), INTENT(INOUT) :: cond_sink

  REAL(dp), INTENT(IN) :: timestep, temperature, pressure, mass_accomm
  
  REAL(dp), DIMENSION(nr_bins), INTENT(INOUT) :: particle_conc
  
  REAL(dp), DIMENSION(2), INTENT(IN) :: cond_vapour  ! [molec m-3], condensing vapour concentrations, which is H2SO4 and organics (ELVOC)
  
  REAL(dp), DIMENSION(nr_bins), INTENT(IN) :: particle_volume
  
  REAL(dp), DIMENSION(nr_bins) :: slip_correction, diffusivity, speed_p,  &
                                  particle_conc_new, particle_volume_new, &
                                  Knudsen_H2SO4, Knudsen_ELVOC,           &
                                  FS_H2SO4, FS_ELVOC,                     &
                                  collision_H2SO4, collision_ELVOC
  
  REAL(dp), DIMENSION(nr_cond) :: diffusivity_gas, speed_gas
  REAL(dp) :: dyn_visc, l_gas, dens_air, fraction_stay, fraction_move, lambda_H2SO4, lambda_ELVOC
  
  INTEGER :: j
  
  dyn_visc = 1.8D-5*(temperature/298D0)**0.85D0  ! dynamic viscosity of air
  dens_air=Mair*pressure/(Rg*temperature)        ! Air density
  l_gas=2D0*dyn_visc/(pressure*SQRT(8D0*Mair/(pi*Rg*temperature))) ! Gas mean free path in air (m)
  
  slip_correction = 1D0+(2D0*l_gas/(diameter))*&
  (1.257D0+0.4D0*exp(-1.1D0/(2D0*l_gas/diameter))) ! Cunninghams slip correction factor (Seinfeld and Pandis eq 9.34) 
  
  diffusivity = slip_correction*kb*temperature/(3D0*pi*dyn_visc*diameter)   ! Diffusivity for the different particle sizes m^2/s
  speed_p = SQRT(8D0*kb*temperature/(pi*particle_mass))                     ! speed of particles (m/s)
  
  diffusivity_gas=5D0/(16D0*Na*molecular_dia**2D0*dens_air)*&
  SQRT(Rg*temperature*Mair/(2D0*pi)*(molar_mass+Mair)/molar_mass)           ! Diffusivity of condensable vapours (m^2 s^-1)
  
  ! Thermal velocity of vapour molecule
  speed_gas=SQRT(8D0*kb*temperature/(pi*molecular_mass)) ! speed of H2SO4 molecule
  
  ! Initialize concentration
  particle_conc_new = 0.0_dp
  ! Last bin not changing
  particle_conc_new(nr_bins) = particle_conc(nr_bins)

  DO j=1, nr_bins
    ! Calculate Kndusen nr for each gas
    lambda_H2SO4 = 3D0 * (diffusivity_gas(1)+ diffusivity(j)) / SQRT(speed_gas(1)**2 + speed_p(j)**2)
    Knudsen_H2SO4(j) = 2.0_dp * lambda_H2SO4 / (diameter(j) + molecular_dia(1))  ! H2SO4

    lambda_ELVOC = 3D0 * (diffusivity_gas(2)+ diffusivity(j)) / SQRT(speed_gas(2)**2 + speed_p(j)**2)
    Knudsen_ELVOC(j) = 2.0_dp * lambda_ELVOC / (diameter(j) + molecular_dia(2))  ! ELVOC
  
    ! Fuchs-Sutugin correction factor for each gas
    FS_H2SO4(j) = (0.75_dp * mass_accomm * (1.0_dp + Knudsen_H2SO4(j))) / &
                  (Knudsen_H2SO4(j)**2.0_dp + Knudsen_H2SO4(j) + &
                  0.283_dp * Knudsen_H2SO4(j) * mass_accomm + 0.75_dp * mass_accomm)

    FS_ELVOC(j) = (0.75_dp * mass_accomm * (1.0_dp + Knudsen_ELVOC(j))) / &
                  (Knudsen_ELVOC(j)**2.0_dp + Knudsen_ELVOC(j) + &
                  0.283_dp * Knudsen_ELVOC(j) * mass_accomm + 0.75_dp * mass_accomm)

    ! Calculate collision rate for H2SO4 and ELVOC molecules with particles
    collision_H2SO4(j) = 2.0_dp * pi * (diameter(j) + molecular_dia(1)) * &
                        (diffusivity(j) + diffusivity_gas(1)) * FS_H2SO4(j) * mass_accomm

    collision_ELVOC(j) = 2.0_dp * pi * (diameter(j) + molecular_dia(2)) * &
                        (diffusivity(j) + diffusivity_gas(2)) * FS_ELVOC(j) * mass_accomm

    ! Update particle volume after condensation
    particle_volume_new(j) = particle_volume(j) &
                            + collision_H2SO4(j) * cond_vapour(1) * molecular_volume(1) * timestep & ! H2SO4 condensation
                            + collision_ELVOC(j) * cond_vapour(2) * molecular_volume(2) * timestep   ! ELVOC condensation
  END DO
  
  ! Use the full-stationary method to divide the particles between the size bins
  DO j = 1, nr_bins-1
    ! Fraction of the particle number concentration that stay in size bin j
    fraction_stay = (particle_volume(j+1) - particle_volume_new(j)) / (particle_volume(j+1) - particle_volume(j))
    ! Fraction of the particle number concentration that move to next size bin j+1
    fraction_move = 1.0_dp - fraction_stay
    ! In size bin 1 to nr_bins-1 to the fixed diameter grid  
    particle_conc_new(j) = particle_conc_new(j) + fraction_stay * particle_conc(j)
    particle_conc_new(j+1) = particle_conc_new(j+1) + fraction_move * particle_conc(j)
  END DO
  ! Update the particle concentration in the particle_conc vector
  particle_conc = particle_conc_new
  cond_sink(1) = sum(particle_conc * collision_H2SO4)
  cond_sink(2) = sum(particle_conc * collision_ELVOC)

END SUBROUTINE condensation

SUBROUTINE coagulation(timestep, particle_conc, diameter, &
                       temperature, pressure, particle_mass)
  
  REAL(dp), DIMENSION(nr_bins), INTENT(IN) :: diameter
  REAL(dp), DIMENSION(nr_bins), INTENT(INOUT) :: particle_conc
  REAL(dp), INTENT(IN) :: timestep
  REAL(dp), DIMENSION(nr_bins), INTENT(IN) :: particle_mass       ! mass of one particle                                 
  REAL(dp), INTENT(IN) :: temperature, pressure
  
  REAL(dp), DIMENSION(nr_bins,nr_bins) :: coagulation_coef        ! coagulation coefficients [m^3/s]
  
  REAL(dp), DIMENSION(nr_bins) :: slip_correction, diffusivity, dist, speed_p, &
                                  Beta_Fuchs, free_path_p, coag_loss
  
  REAL(dp) :: dyn_visc, &  ! dynamic viscosity, kg/(m*s)
              l_gas,    &  ! Gas mean free path in air
              loss1,    &  ! Self coagulation
              loss2        ! Coagulation with larger particles
  
  INTEGER  :: i, j
  
  ! The coagulation coefficient is calculated according to formula 13.56 in Seinfield and Pandis (2006), Page 603
  
  dyn_visc = 1.8D-5*(temperature/298.0d0)**0.85                                           ! Dynamic viscosity of air
  
  l_gas=2D0*dyn_visc/(pressure*SQRT(8D0*Mair/(pi*Rg*temperature)))                        ! Gas mean free path in air (m)
  
  slip_correction = 1D0+(2D0*l_gas/(diameter))*&
  (1.257D0+0.4D0*exp(-1.1D0/(2D0*l_gas/diameter)))                                        ! Cunninghams slip correction factor (Seinfeld and Pandis eq 9.34)
  
  diffusivity = slip_correction*kb*temperature/(3D0*pi*dyn_visc*diameter)                 ! Diffusivity for the different particle sizes m^2/s
  
  speed_p = SQRT(8D0*kb*temperature/(pi*particle_mass))                                   ! Speed of particles (m/s)
  
  free_path_p = 8D0*diffusivity/(pi*speed_p)                                              ! Particle mean free path (m)
  
  dist = (1D0/(3D0*diameter*free_path_p))*((diameter+free_path_p)**3D0 &
  -(diameter**2D0+free_path_p**2D0)**(3D0/2D0))-diameter                                  ! mean distance from the center of a sphere reached by particles leaving the sphere's surface (m)

  DO i = 1,nr_bins
     Beta_Fuchs = 1D0/((diameter+diameter(i))/(diameter+diameter(i)+&
     2D0*(dist**2D0+dist(i)**2D0)**0.5D0)+8D0*(diffusivity+diffusivity(i))/&
     (((speed_p**2D0+speed_p(i)**2D0)**0.5D0)*(diameter+diameter(i))))                    ! Fuchs correction factor from Seinfeld and Pandis, 2006, p. 600
  
     coagulation_coef(i,:) = 2D0*pi*Beta_Fuchs*(diameter*diffusivity(i)+&
     diameter*diffusivity+diameter(i)*diffusivity+diameter(i)*diffusivity(i))             ! coagulation rates between two particles of all size combinations  (m^3/s)    
  END DO

  ! Initialize the coagulation loss term
  coag_loss = 0.0D0

  ! Compute self-coagulation (loss1): coagulation within the same bin
  DO i = 1, nr_bins
     loss1 = coagulation_coef(i,i) * particle_conc(i) * particle_conc(i)
     coag_loss(i) = coag_loss(i) + loss1
  END DO

  ! Compute coagulation with particles in different bins (loss2)
  DO i = 1, nr_bins-1
     DO j = i+1, nr_bins
      loss2 = coagulation_coef(i,j) * particle_conc(i) * particle_conc(j)
      coag_loss(i) = coag_loss(i) + loss2
     END DO
  END DO

  ! Calculate the change in particle concentration due to coagulation
  DO i = 1, nr_bins
     ! The concentration decreases due to coagulation
     particle_conc(i) = particle_conc(i) - coag_loss(i) * timestep
  END DO  
END SUBROUTINE coagulation

  
SUBROUTINE dry_dep_velocity(temperature, pressure, DSWF, & 
                            Richards_nr10m, wind_speed10m, vd_gas, vd_particle)
  REAL(dp), INTENT(IN) :: temperature   , &   ! Air temperature [K] at reference height
                          pressure      , &   ! Air pressure [Pa] at reference height
                          Richards_nr10m, &   ! Richardson number at 10m (stability)
                          DSWF          , &   ! Downward shortwave radiation flux [W m-2]
                          wind_speed10m       ! Wind speed [m s-1] at 10m
  REAL(dp) :: z0m, r_coll, a_landuse, j_landuse, v_kinematic, dyn_visc, lambda_air, Pr, beta, &
              gam, zr, u_friction, dens_air, L_Ob, rj
              
  ! Variables for particles
  REAL(dp), DIMENSION(nr_bins) :: St, Schmidt_particle, sed_v, diffusivity_particle, &
                                  slip_correction, z_rough_particle, &
                                  ra_particle, rb_particle, Scf_rough_particle
  REAL(dp), DIMENSION(nr_bins), INTENT(OUT) :: vd_particle
  real(dp) :: Scf_zr
  INTEGER :: i 

  ! Variables for gases
  INTEGER, PARAMETER :: num_gases = 5 ! Indexes: SO2: 1, O3: 2, HNO3: 3, isoprene: 4, apinene: 5
  REAL(dp), DIMENSION(num_gases) :: Diffusivity_gas, z_rough_gas, Scf_rough_gas, ra_gas, schmidt_gas, rb_gas, &
                                    rsm_gas, rlu_gas, rcl_gas, rgs_gas, rc_gas, &
                                    D_ratio, H_eff, f0
  REAL(dp), DIMENSION(num_gases), INTENT(OUT) :: vd_gas                                  
  REAL(dp) :: DiffusivityH2O, rst_h2o, rdc, rac, rlu
  INTEGER :: j
       
  
  dens_air = Mair*pressure/(Rg*temperature)    ! Air density (kg/m^3)
  dyn_visc = 1.8D-5*(temperature/298.)**0.85   ! dynamic viscosity of air (kg/(m*s))
  v_kinematic = dyn_visc/dens_air              ! kinematic viscosity of air (m^2/s)
  lambda_air = 2D0*dyn_visc/(pressure*SQRT(8D0*Mair/(pi*Rg*temperature))) ! Gas mean free path in air (m)
  slip_correction = 1D0+(2D0*lambda_air/(diameter))*(1.257D0+0.4D0*exp(-1.1D0/(2D0*lambda_air/diameter))) ! Cunninghams slip correction factor (Seinfeld and Pandis eq 9.34)
  diffusivity_particle = slip_correction*kb*temperature/(3D0*pi*dyn_visc*diameter) ! Diffusivity for the different particle sizes m^2/s

  zr = 10D0                   ! Reference height [m]
  L_Ob = zr / Richards_nr10m  ! Monin-Obukhov length scale
  z0m = 0.9D0             ! Surface roughness length for momentum evergreen, needleleaf trees (m)     
  u_friction = ka * wind_speed10m / (log(zr/z0m))  ! Friction velocity (Eq. 16.67 from Seinfeld and Pandis, 2006)

  ! Land use category paramaters from Seinfeld and Pandis, 2006 Table 19.2: 
  r_coll = 2D-3 ! radius of collector evergreen, needleleaf trees

  ! coefficients based on land use categories (evergreen, needleleaf trees)
  a_landuse = 1D0
  j_landuse = 0.56D0

  Pr = 0.95D0   ! Turbulent Prandtl number (when ka = 0.4 (Hogstrom, 1988))
  beta = 7.8D0  ! When ka = 0.4 (Hogstrom, 1988)
  gam = 11.6D0  ! When ka = 0.4 (Hogstrom, 1988)

  ! Stability correction factor at 10 m
  if (Richards_nr10m < -1D-6) then
    Scf_zr = (SQRT(1.0_dp - gam * zr / L_Ob) - 1.0_dp) / (SQRT(1.0_dp - gam * zr / L_Ob) + 1.0_dp)  
  end if

  do i=1, nr_bins
    ! Calculate the particle sedimentation velocity (m/s):
    sed_v(i) = ((diameter(i)**2) * (particle_density - dens_air) * g * slip_correction(i)) / (18.0_dp * dyn_visc)
    ! Calculation of aerodynamic resistance (r_a) for particles for:
    z_rough_particle(i) = diffusivity_particle(i) / (ka * u_friction)   ! surface roughness length scale for particles

    if (Richards_nr10m > 1D-6) then  ! stable boundary layer (Ri>1D-6)
      ra_particle(i) = (Pr * LOG(zr / z_rough_particle(i)) + beta / L_Ob * (zr - z_rough_particle(i))) / (ka * u_friction)
    else if (Richards_nr10m < -1D-6) then  ! unstable boundary layer Ri<-1D-6
      ! Stability correction factor at surface roughness length scale for molecules or particles
      Scf_rough_particle(i) = (SQRT(1.0_dp - gam * z_rough_particle(i) / L_Ob ) - 1.0_dp) &
                              / (SQRT(1.0_dp - gam * z_rough_particle(i) / L_Ob ) + 1.0_dp)
      ra_particle(i) = Pr * LOG(Scf_zr / Scf_rough_particle(i)) / (ka * u_friction)
    else ! Neutral (implicitly >= -1E-6 and <= 1E-6)
      ra_particle(i) = Pr * LOG(zr / z_rough_particle(i)) / (ka * u_friction) 
    end if
    
    ! Calculate the quasi-laminar resistance (r_b) for particles s/m:
    St(i) = sed_v(i) * u_friction / g / r_coll ! Stokes nr of vegetation
    Schmidt_particle(i) = v_kinematic / diffusivity_particle(i)
    rb_particle(i) = (3.0_dp * u_friction * EXP(-SQRT(St(i))) &
                    * (Schmidt_particle(i)**(-j_landuse)  &
                    + (St(i) / (a_landuse + St(i)))**2.0_dp &
                    + 0.5_dp*(diameter(i)/r_coll)**2.0_dp))**(-1.0_dp)
    
    ! Calculate the dry deposition velocity for particles:
    vd_particle(i) = 1.0_dp / (ra_particle(i) + rb_particle(i) + ra_particle(i) * rb_particle(i) * sed_v(i)) + sed_v(i)
  end do

  ! Calculate the dry deposition velocity for O3, SO2, HNO3, isoprene and a-pinene: 
  ! Diffusion coefficients of selected gases
  DiffusivityH2O = 0.234D-4 ! Diffusion coefficient of water vapor in air (m^2/s), table 16.2 Seinfeld and Pandis
  ! ratio between diffusivity of water vapor and SO2, O3 or HNO3 from table 19.4 Seinfeld and Pandis
  D_ratio(1) = 1.89D0      ! SO2
  D_ratio(2) = 1.63D0      ! O3
  D_ratio(3) = 1.87D0      ! HNO3
  D_ratio(4) = 2.7D0       ! isoprene (estimated)
  D_ratio(5) = 4.0D0       ! apinene (estimated)

  do j=1, num_gases
    Diffusivity_gas(j) = DiffusivityH2O / D_ratio(j)
  end do
  
  ! Calculate the aerodynamic resistance for O3, SO2, HNO3, isoprene & a-pinene (ra) in similar way as
  ! for particles:
  do j=1, num_gases
    ! Calculate surface roughness length scale for all gases
    z_rough_gas(j) = Diffusivity_gas(j) / (ka * u_friction)
  end do
  
  if (Richards_nr10m > 1D-6) then ! stable boundary layer (Ri>1D-6)
    do j=1, num_gases
      ra_gas(j) = (Pr * LOG(zr / z_rough_gas(j)) + beta / L_Ob * (zr - z_rough_gas(j))) / (ka * u_friction)
    end do

  else if (Richards_nr10m < -1D-6) then ! unstable boundary layer Ri<-1D-6
    ! Stability correction factor at surface roughness length scale for molecules
    do j=1, num_gases
      Scf_rough_gas(j) = (SQRT(1 - gam * z_rough_gas(j) / L_Ob ) - 1) / (SQRT(1 - gam * z_rough_gas(j) / L_Ob ) + 1)
      ra_gas(j) = Pr * LOG(Scf_zr / Scf_rough_gas(j)) / (ka * u_friction)
    end do
 
  else  ! neutral boundary layer (abs(Ri)<1D-6
    do j=1, num_gases
      ra_gas(j) = Pr * LOG(zr / z_rough_gas(j)) / (ka * u_friction) 
    end do
  end if

  ! Calculate the quasi-laminar resistance for O3, SO2, HNO3, isoprene & a-pinene (rb):
  do j=1, num_gases
    schmidt_gas(j) = v_kinematic / Diffusivity_gas(j)
    rb_gas(j) = 5.0_dp * schmidt_gas(j)**(2.0_dp/3.0_dp) / u_friction
  end do
  
  ! Calculation of surface resistance for O3, SO2, HNO3, isoprene & a-pinene (rc)
  ! Effective Henry's lay const:
  H_eff(1) = 1D5    ! SO2, M atm^-1
  H_eff(2) = 1D-2   ! O3, M atm^-1
  H_eff(3) = 1D14   ! HNO3, M atm^-1
  H_eff(4) = 1.2D-2 ! isoprene, M atm^-1
  H_eff(5) = 3D-2   ! apinene, M atm^-1
  
  ! Noramlized reactivity, table 19.4 from Seinfeld and Pandis, 2006:
  f0 = 0D0    ! All equal to zero, exept for O3
  f0(2) = 1D0 ! O3
  
  ! Calculate the bulk canopy stomatal resistance (rst)
  rj = 130D0 ! (s/m) Summer, evergreen, needleleaf. The minimum, bulk canopy stomatal resistance for water vapor
  rst_h2o = rj * (1 + (200.0_dp / (DSWF + 0.1_dp))**2.0_dp * 400.0_dp / ((temperature-273.15_dp) * (40.0_dp - (temperature-273.15_dp))))
  
  ! The resistance of the outer surfaces in the upper canopy ???
  rlu = 2000D0 ! (s/m) Summer, evergreen, needleleaf
  do j=1, num_gases
    ! Calculate the combined stomatal and mesophyll resistance (rsm):
    rsm_gas(j) = rst_h2o * DiffusivityH2O / Diffusivity_gas(j) + 1.0_dp / (3.3D-4 * H_eff(j) + 100.0_dp * f0(j))
    ! Calculate the resistance of the outer surfaces in the upper canopy (rlu):
    rlu_gas(j) = rlu / (1D-5 * H_eff(j) + f0(j))
  end do

  ! resistance for uptake by soil, leaf litter at the ground; (s/m) Summer, evergreen, needleleaf
  rgs_gas(1) = 500D0 ! SO2
  rgs_gas(2) = 200D0 ! O3
  ! resistance for uptake by leaves,twigs, and other exposed surfaces; (s/m) Summer, evergreen, needleleaf 
  rcl_gas(1) = 2000D0 ! SO2 
  rcl_gas(2) = 1000D0 ! O3 
  do j=3, num_gases
    ! Calculate the resistance of the exposed surfaces in the lower portions of 
    ! structures of the canopy (rcl): 
    rcl_gas(j) = (1D-5 * H_eff(j) / rcl_gas(1) + f0(j) / rcl_gas(2))**(-1.0_dp)
    ! Calculate the resistance of the exposed surfaces on the groud 
    !(soil,leaf litter, ground) (rgs):
    rgs_gas(j) = (1D-5 * H_eff(j) / rgs_gas(1) + f0(j) / rgs_gas(2))**(-1.0_dp)
  end do

  ! Calculate the resistance to transfer by buoyant convection (rdc):
  rdc = 100.0_dp * (1.0_dp + 1000.0_dp / (DSWF + 10.0_dp))
  ! transfer resistance on the ground (that depends only on canopy height)
  rac = 2000D0 ! (s/m) Summer, evergreen, needleleaf
  do j=1, num_gases
    ! Combine all resistances in order to get the total surface resistance 
    ! for O3, SO2, HNO3, isoprene and a-pinene (rc):
    rc_gas(j) = (1/rsm_gas(j) + 1/rlu_gas(j) + 1/(rdc+rcl_gas(j)) + 1/(rgs_gas(j)+rac))**(-1.0_dp)
  end do
   
  ! Finally calculate the dry deposition velocity of SO2, O3, HNO3, isoprene and a-pinene:
  do j=1, num_gases
    vd_gas(j) = 1 / (ra_gas(j) + rb_gas(j) + rc_gas(j))
  end do

END SUBROUTINE dry_dep_velocity

END MODULE aerosol_mod