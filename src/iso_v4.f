c   ISO fortran Routines and Functions: Version 5.0 
c   Written by: Randy Millerson

       program isovalues
       implicit real*8(a-h,o-z)

       common/maineos/xdata(100),zdata(100)
     1                 xsnm(100), ydata(100)
     2                 breakz(100),cscoefz(4,100),
     3                 breaky(100),cscoefy(4,100),
     4                 xdatas(100),xdatan(100)
       common/mainiso/n,n0,n1,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100)

       common/pareos/n_read
       common/paremp/mic,isnm,isym_emp,k0,rho0

       call readISO()
       call getISO(0)

       stop
       end program


c      Subroutine to read in EoS, run this first for the ISO routine
       subroutine readISO()
c      creates a series of splines for the input nuclear EoS.
c      Splines created are den vs. energy-per-particle for both
c      symmetric and neutron matter as well as den vs. pressure

       implicit real*8(a-h,o-z)
       common/maineos/xdata(100),zdata(100)
     1                 xsnm(100), ydata(100)
     2                 breakz(100),cscoefz(4,100),
     3                 breaky(100),cscoefy(4,100),
     4                 xdatas(100),xdatan(100)
       common/mainiso/n,n0,n1,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100)

       common/pareos/n_read
       common/paremp/mic,isnm,isym_emp,k0,rho0
       common/factor/pi,pi2

       pi=3.141592654d0 
       pi2=pi*pi

c       open(unit=000,file='dump.don')
       open(unit=515,file='readpar.don')
       open(unit=616,file='phenpar.don')
       open(unit=919,file='IsoVals.don')

c      n, n0, and n1 must be greater than 3 if greater not equal to 0.
       read(515,*) n_read, nkf_read, n, n0, n1,
       read(616,*) mic, isnm, isym_emp, k0, rho0

       if(n_read .eq. 0) then
          open(unit=14,file='ex_nxlo.don')
          do i=1,n0
             read(14,*) xkf, ydata(i), zdata(i)
             if(nkf_read .eq. 1) then
                xdatas(i) = (2.d0/3.d0)*xkf*xkf*xkf/pi2
             else if(nkf_read .eq. 0) then
                xdatas(i) = xkf
             end if
             easym(i) = zdata(i)-ydata(i)
          end do
       else if(n_read .eq. 1) then
          open(unit=14, file='e0_nxlo.don') 
          open(unit=15, file='e1_nxlo.don')
          do i=1,n0
             read(14,*) xkfs, ydata(i)
             if(nkf_read .eq. 1) then
                xdatas(i) = (2.d0/3.d0)*xkfs*xkfs*xkfs/pi2
             else if(nkf_read .eq. 0) then
                xdatas(i) = xkfs
             end if
          end do
          do i=1,n1
             read(15,*) xkfn, zdata(i)
             if(nkf_read .eq. 1) then
                xdatan(i) = (1.d0/3.d0)*xkfn*xkfn*xkfn/pi2
             else if(nkf_read .eq. 0) then
                xdatan(i) = xkfn
             end if
          end do
       end if

       if(n .gt. 0) then
          open(unit=17, file='den.don')
          do i=1,n0
             read(14,*) den(i)
             xdatas(i)= (2.d0/3.d0)*xkf*xkf*xkf/pi2
          end do 
       end if

       if(mic .eq. 0) then
          if(n_read .eq. 0) then
             do i=1,n0
                ydata(i) = e0_val(xdatas(i))
             end do
          end if
       end if

       if(mic .eq. 0) then
          if(n_read .eq. 0 .or. n_read .eq. 2) then
             do i=1,n0
                ydata(i) = e0_val(xdatas(i))
             end do
          end if
       end if

c       set up EoS interpolation
       if(n_read .eq. 0) then
          call dcsakm(n,xdatas,ydata,breaky,cscoefy)
          call dcsakm(n,xdatas,zdata,breakz,cscoefz)
          call dcsakm(n,xdatas,easym,breaks,cscoefs)
       else if(n_read .eq. 1) then
          call dcsakm(n1,xdatan,zdata,breakz,cscoefz)
          call dcsakm(n0,xdatas,ydata,breaky,cscoefy)
          do i=1,n0
             e1temp = dcsval(xdatas(i),n1-1,breakz,cscoefz) 
             easym(i) = e1temp-ydata(i) 
          end do
          call dcsakm(n0,xdatas,easym,breaks,cscoefs)
       end if

       end



!      Routine to set up interpolation of the nuclear EoS
       subroutine getISO(nswitch)
       implicit real*8(a-h,o-z)

       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm,
     1                 breakz(75),cscoefz(4,75),
     2                 breaky(75),cscoefy(4,75),
     4                 xdatas(100),xdatan(100)
       common/mainiso/n,n_0,n_1,
     1                easym(75),breaks(75),cscoefs(4,75),
     2                den(75),breaka(75),cscoefa(4,75),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100)
       common/isovals/desym(100),de0(100),de1(100),
     1                prse0(100),prse1(100),prsesym(100)

       common/pareos/n_read
       common/paremp/mic,isnm,isym_emp,k0,rho0
       common/factor/pi,pi2

       nexit = 0
       if(nswitch .lt. 0 .or. nswitch .gt. 2) then 
           goto 9999
       else if (nswitch .eq. 0) then 
           nexit = 0
       else if(nswitch .eq. 1) then
           nexit = nswitch
       else if(nswitch .eq. 2) then
           nexit = nswitch
       end if 

c      Pressure & Iso-value interpolation
       if(n_read .eq. 0) then
          do i=1,n
            desym(i) = dcsder(1,xdata(i),n2,breaks,cscoefs)
            de0(i) = dcsder(1,xdata(i),n2,breaky,cscoefy)
            de1(i) = dcsder(1,xdata(i),n2,breakz,cscoefz)
            prse0(i) = xdata(i)*xdata(i)*de0(i)   
            prse1(i) = xdata(i)*xdata(i)*de1(i)
            prsesym(i) = xdata(i)*xdata(i)*desym(i) 
          end do
          call dcsakm(n,de0,xdata,breakd,coeffd)
          call dcsakm(n,xdata,prse0,breakp0,coeffp0)
          call dcsakm(n,xdata,prse1,breakp1,coeffp1)
       else if(n_read .eq. 1) then
          if(n .gt. 3) then
             do i=1,n
                desym(i) = dcsder(1,xdata(i),n2,breaks,cscoefs)
                de0(i) = dcsder(1,xdata(i),n_0-1,breaky,cscoefy)
                de1(i) = dcsder(1,xdata(i),n_1-1,breakz,cscoefz)
                prse0(i) = xdata(i)*xdata(i)*de0(i)   
                prse1(i) = xdata(i)*xdata(i)*de1(i)
                prsesym(i) = xdata(i)*xdata(i)*desym(i) 
             end do
             call dcsakm(n,de0,xdata,breakd,coeffd)
             call dcsakm(n,xdata,prse0,breakp0,coeffp0)
             call dcsakm(n,xdata,prse1,breakp1,coeffp1)
          else
             do i=1,n_0
                desym(i) = dcsder(1,xdatas(i),n_0-1,breaks,cscoefs)
                de0(i) = dcsder(1,xdatas(i),n_0-1,breaky,cscoefy)
                prse0(i) = xdatas(i)*xdatas(i)*de0(i)   
                prsesym(i) = xdatas(i)*xdatas(i)*desym(i)
             end do
             do i=1,n_1
                de1(i) = dcsder(1,xdatan(i),n_1-1,breakz,cscoefz)
                prse1(i) = xdatan(i)*xdatan(i)*de1(i)
             end do
             call dcsakm(n_0,de0,xdatas,breakd,coeffd)
             call dcsakm(n_0,xdatas,prse0,breakp0,coeffp0)
             call dcsakm(n_1,xdatan,prse1,breakp1,coeffp1)
          end if
       else if(n_read .eq. 2) then
          do i=1,n
             desym(i) = dcsder(1,xdata(i),n2,breaks,cscoefs)
             de0(i) = dcsder(1,xdata(i),n2,breaky,cscoefy)
             prse0(i) = xdata(i)*xdata(i)*de0(i)   
             prsesym(i) = xdata(i)*xdata(i)*desym(i) 
          end do
          call dcsakm(n,de0,xdata,breakd,coeffd)
          call dcsakm(n,xdata,prse0,breakp0,coeffp0)
       end if

       if(nexit .eq. 1) then 
           goto 9999
       end if


       if(n_read .eq. 0) then
          rho1 = 0.1d0
          rho0 = dcsval(0.d0,n2,breakd,coeffd)
          rho2 = 2.d0*rho0

          e0o = dcsval(rho0,n2,breaky,cscoefy)
          e01 = dcsval(rho1,n2,breaky,cscoefy)
          e02 = dcsval(rho2,n2,breaky,cscoefy)

          e1o = dcsval(rho0,n2,breakz,cscoefz)
          e11 = dcsval(rho1,n2,breakz,cscoefz)
          e12 = dcsval(rho2,n2,breakz,cscoefz)

          prs0o = dcsval(rho0,n2,breakp0,coeffp0)
          prs01 = dcsval(rho1,n2,breakp0,coeffp0)
          prs02 = dcsval(rho2,n2,breakp0,coeffp0)

          prs1o = dcsval(rho0,n2,breakp1,coeffp1)
          prs11 = dcsval(rho1,n2,breakp1,coeffp1)
          prs12 = dcsval(rho2,n2,breakp1,coeffp1)

          esym0 = dcsval(rho0,n2,breaks,cscoefs)
          esym1 = dcsval(rho1,n2,breaks,cscoefs)
          esym2 = dcsval(rho2,n2,breaks,cscoefs)

          bigL = 3.d0*rho0*dcsder(1,rho0,n2,breaks,cscoefs) 
          bigK = 9.d0*rho0*rho0*dcsder(2,rho0,n2,breaks,cscoefs)
          bigKR= 9.d0*rho1*rho1*dcsder(2,rho1,n2,breaks,cscoefs)
          bigK0= 9.d0*rho0*rho0*dcsder(2,rho0,n2,breaky,cscoefy)

       else if(n_read .eq. 1) then
          if(n .gt. 3) then
             rho1 = 0.1d0
             rho0 = dcsval(0.d0,n2,breakd,coeffd)
             rho2 = 2.d0*rho0

             e0o = dcsval(rho0,n_0-1,breaky,cscoefy)
             e01 = dcsval(rho1,n_0-1,breaky,cscoefy)
             e02 = dcsval(rho2,n_0-1,breaky,cscoefy)

             e1o = dcsval(rho0,n_1-1,breakz,cscoefz)
             e11 = dcsval(rho1,n_1-1,breakz,cscoefz)
             e12 = dcsval(rho2,n_1-1,breakz,cscoefz)

             prs0o = dcsval(rho0,n2,breakp0,coeffp0)
             prs01 = dcsval(rho1,n2,breakp0,coeffp0)
             prs02 = dcsval(rho2,n2,breakp0,coeffp0)

             prs1o = dcsval(rho0,n2,breakp1,coeffp1)
             prs11 = dcsval(rho1,n2,breakp1,coeffp1)
             prs12 = dcsval(rho2,n2,breakp1,coeffp1)
		     
             esym0 = dcsval(rho0,n2,breaks,cscoefs)
             esym1 = dcsval(rho1,n2,breaks,cscoefs)
             esym2 = dcsval(rho2,n2,breaks,cscoefs)

             bigL = 3.d0*rho0*dcsder(1,rho0,n2,breaks,cscoefs) 
             bigK = 9.d0*rho0*rho0*dcsder(2,rho0,n2,breaks,cscoefs)
             bigKR = 9.d0*rho1*rho1*dcsder(2,rho1,n2,breaks,cscoefs)
             bigK0 = 9.d0*rho0*rho0*dcsder(2,rho0,n2,breaky,cscoefy)
          else
             rho1 = 0.1d0
             rho0 = dcsval(0.d0,n_0-1,breakd,coeffd)
             rho2 = 2.d0*rho0

             e0o = dcsval(rho0,n_0-1,breaky,cscoefy)
             e01 = dcsval(rho1,n_0-1,breaky,cscoefy)
             e02 = dcsval(rho2,n_0-1,breaky,cscoefy)

             e1o = dcsval(rho0,n_1-1,breakz,cscoefz)
             e11 = dcsval(rho1,n_1-1,breakz,cscoefz)
             e12 = dcsval(rho2,n_1-1,breakz,cscoefz)

             prs0o = dcsval(rho0,n_0-1,breakp0,coeffp0)
             prs01 = dcsval(rho1,n_0-1,breakp0,coeffp0)
             prs02 = dcsval(rho2,n_0-1,breakp0,coeffp0)

             prs1o = dcsval(rho0,n_1-1,breakp1,coeffp1)
             prs11 = dcsval(rho1,n_1-1,breakp1,coeffp1)
             prs12 = dcsval(rho2,n_1-1,breakp1,coeffp1)

             esym0 = dcsval(rho0,n_0-1,breaks,cscoefs)
             esym1 = dcsval(rho1,n_0-1,breaks,cscoefs)
             esym2 = dcsval(rho2,n_0-1,breaks,cscoefs)

             bigL = 3.d0*rho0*dcsder(1,rho0,n_0-1,breaks,cscoefs) 
             bigK = 9.d0*rho0*rho0*dcsder(2,rho0,n_0-1,breaks,cscoefs)
             bigKR = 9.d0*rho1*rho1*dcsder(2,rho1,n_0-1,breaks,cscoefs)
             bigK0 = 9.d0*rho0*rho0*dcsder(2,rho0,n_0-1,breaky,cscoefy)
          end if
       else if(n_read .eq. 2) then
          rho1 = 0.1d0
          rho0 = dcsval(0.d0,n2,breakd,coeffd)
          rho2 = 2.d0*rho0

          e0o = dcsval(rho0,n2,breaky,cscoefy)
          e01 = dcsval(rho1,n2,breaky,cscoefy)
          e02 = dcsval(rho2,n2,breaky,cscoefy)

          prs0o = dcsval(rho0,n2,breakp0,coeffp0)
          prs01 = dcsval(rho1,n2,breakp0,coeffp0)
          prs02 = dcsval(rho2,n2,breakp0,coeffp0)

          esym0 = e0o
          esym1 = e01
          esym2 = e02

          bigL = 3.d0*rho0*dcsder(1,rho0,n2,breaks,cscoefs) 
          bigK = 9.d0*rho0*rho0*dcsder(2,rho0,n2,breaks,cscoefs)
          bigKR = 9.d0*rho1*rho1*dcsder(2,rho1,n2,breaks,cscoefs)
          bigK0 = bigKR
       end if

       if(nexit .eq. 2) then 
           goto 9999
       end if

       if(n_read .ne. 2) then 
          write(919,*) "Iso-values: Isovector and Isoscalar values" 
          write(919,*) " "
          write(919,*) "  Rho0   Rho1   Rho2"
          write(919,2020) rho0, rho1, rho2
          write(919,*) " "
          write(919,*) "  e0o      e01      e02"
          write(919,2021) e0o, e01, e02
          write(919,*) " "
          write(919,*) "  e1o      e11      e12"
          write(919,2021) e1o, e11, e12
          write(919,*) " "
          write(919,*) "  prs0o    prs01    prs02"
          write(919,2021) prs0o, prs01, prs02
          write(919,*) " "
          write(919,*) "  prs1o    prs11    prs12"
          write(919,2021) prs1o, prs11, prs12
          write(919,*) " "
          write(919,*) "  esym0    esym1    esym2"
          write(919,2021) esym0, esym1, esym2
          write(919,*) " "
          write(919,*) "  L         K         KD        K0"
          write(919,2022) bigL, bigK, bigKR, bigK0
          write(919,*) " "
          write(919,*) " "
       else
          write(919,*) "Iso-values: Isovector and Isoscalar values" 
          write(919,*) " "
          write(919,*) "  Rho0    Rho1   Rho2"
          write(919,2020) rho0, rho1, rho2
          write(919,*) " "
          write(919,*) "  e0o      e01      P0"
          write(919,2021) e0o, e01, prs0
          write(919,*) " "
          write(919,*) "  prs0o    prs01    prs02"
          write(919,2021) prs0o, prs01, prs02
          write(919,*) " "
          write(919,*) "  L         K         KD        K0"
          write(919,2022) bigL, bigK, bigKR, bigK0
          write(919,*) " "
          write(919,*) " "
       end if


2020   format(2x,F6.3,2x,F6.3,2x,F6.3)
2021   format(2x,F7.3,2x,F7.3,2x,F7.3)
2022   format(1x,F8.3,2x,F8.3,2x,F8.3,2x,F8.3)
9999   return           
       end 


       subroutine parab(nprint)
c      Generates six equations of state for infinite 
c      nuclear matter at various densities but with 
c      increasing asymmetry ranging from symmetric 
c      to pure neutron matter

       implicit real*8(a-h,o-z)
       common/eos/xkf(100),den(100),e0(100),e1(100),esym(100)
       common/factor/pi,pi2
        
       dimension :: ea(6,100), alp(6)

       open(777,file='parab.don')

       pi=3.14159d0
       pi2 = pi*pi

       do i=1,6 
          alp(i) = 0.d0 + 0.2d0 * (i-1)
       end do

       do j=1,6
          do i=1,n
             ea(j,i) = e0(i)+esym(i)*alp(j)**2 
          end do
       end do

       write(777,*) '   den      ea0       ea2       ea4       ea6
     1ea8       ea1'
       do i=1,n
          write(777,1414) den(i), ea(1,i), ea(2,i),
     1                    ea(3,i), ea(4,i), ea(5,i), ea(6,i)
       end do

1414   format(2x,F8.4,2x,F8.4,2x,F8.4,2x,F8.4,2x,F8.4,
     1        2x,F8.4,2x,F8.4)

       end subroutine

       function eafff(rho)
       implicit real*8(a-h,o-z)
        
       a1=119.14d0
       b1=-816.95d0
       c1=724.51d0
       d1=-32.99d0
       d2=891.15d0
       ff1=a1*2.d0*(0.5d0)**(5.d0/3.d0)
       ff2=d1*2.d0*(0.5d0)**(5.d0/3.d0) + 
     1     d2*2.d0*(0.5d0)**(8.d0/3.d0) 
         
       alph=0.2d0 
        
       ee=ff1*(rho)**(2.d0/3.d0) + b1*rho +
     1 c1*(rho)**(alph+1.d0) + ff2*(rho)**(5.d0/3.d0) 

       eafff = ee
       end   


       function earat(rho)
       implicit real*8(a-h,o-z)
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0

       pi=3.141592654d0 
       pi2=pi*pi
       
       rat=rho/rho0
        
       fact=(3.d0*pi2/2.d0)**(2.d0/3.d0) 
       hbc=197.327d0
       hbc2=hbc**2
       xm=938.926d0 
       tfact=(3.d0*hbc2/10.d0/xm)
       totfact=fact*tfact
           
       alpha=-29.47-46.74*(k0+44.21)/(k0-166.11)
       beta=23.37*(k0+254.53)/(k0-166.11)       
       sigma=(k0+44.21)/210.32                   
        
       earat = totfact*(datapt)**(2.d0/3.d0) + (alpha/2.d0)*(rat)+
     1    (beta/(sigma + 1.d0))*(rat)**(sigma) 
        
       end 


       function e0_val(rho)
       implicit real*8(a-h,o-z)
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm, 
     1                 breakz(75),cscoefz(4,75),       
     2                 breaky(75),cscoefy(4,75),  
     4                 xdatas(100),xdatan(100)
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff

c      Calculates the energy-per-particle for symmetric nuclear matter from a density

       nintv=nxdata-1

c      phenom_eos_section
       if(mic.eq.0) then 
       
          if(isnm.eq.1) then
             e0=eafff(rho) 
          else 
             e0=earat(rho) 
          end if 
       
          if(rho.le.0.0019.and.e0.gt.0.d0) then
             e0=0.d0 
          end if

       else 
          e0=dcsval(rho,nintv,breaky,cscoefy)            
       end if
         
       e0_val = e0 
       end   


       function e1_val(rho)
       implicit real*8(a-h,o-z)
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm, 
     1                 breakz(75),cscoefz(4,75),       
     2                 breaky(75),cscoefy(4,75),  
     4                 xdatas(100),xdatan(100)
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff

c      Calculates the energy-per-particle for neutron nuclear matter from a density
c      intialization (calling init) is assumed

       nintv2=nxnm-1 
       e1_val = dcsval(rho,nintv2,breakz,cscoefz)
       end   


       function esym_ph(rho, gam)
       implicit real*8(a-h,o-z)
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
           
       rat=rho/rho0       
       esym_ph = 22.d0*rat**gam + 12.d0*rat**(2.d0/3.d0) 
       end 

