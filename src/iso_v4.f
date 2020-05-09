c   ISO fortran Routines and Functions: Version 5.0 
c   Written by: Dalcoin

       program isovalues
       implicit real*8(a-h,o-z)

       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm,
     1                 breakz(75),cscoefz(4,75),
     2                 breaky(75),cscoefy(4,75),
     4                 xdatas(100),xdatan(100)
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm,
     1                 breakz(75),cscoefz(4,75),
     2                 breaky(75),cscoefy(4,75),
     4                 xdatas(100),xdatan(100)

       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       common/readpar/n_read

       common/pariso/nrho_ref, rho1, rho_ref(100)

       call readISO()
       call getISO(0)

       stop
       end program


!      Subroutine to read in EoS, run this first for the ISO routine
       subroutine readISO()
c      creates a series of splines for the input nuclear EoS.
c      Splines created are den vs. energy-per-particle for both
c      symmetric and neutron matter as well as den vs. pressure

       implicit real*8(a-h,o-z)
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm,
     1                 breakz(75),cscoefz(4,75),
     2                 breaky(75),cscoefy(4,75),
     4                 xdatas(100),xdatan(100)
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm,
     1                 breakz(75),cscoefz(4,75),
     2                 breaky(75),cscoefy(4,75),
     4                 xdatas(100),xdatan(100)

       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       common/readpar/n_read
       common/factor/pi,pi2

       common/pariso/nrho_ref, rho1, rho_ref(100)

       pi=3.141592654d0 
       pi2=pi*pi

c       open(unit=000,file='dump.don')
       open(unit=515,file='par.don')
       open(unit=525,file='refpar.don')
       open(unit=919,file='IsoVals.don')

       read(515,*) n, n_den, n_read, n_0, n_1,
     1             mic,isnm,isym_emp,k0,rho0,fff

       read(525,*) nrho_ref, rho1
       if(nrho_ref .gt. 0) then
          do i=1,n
             read(525,*) rho_ref(i)
          end do
       end if

       if(n_read .eq. 0) then
          open(unit=14,file='ex_nxlo.don')
          nxdata = n
          nxnm = n 
       else if(n_read .eq. 1) then 
          open(unit=14, file='e0_nxlo.don') 
          open(unit=15, file='e1_nxlo.don')
          nxdata = n_0
          nxnm = n_1
          if(n .gt. 3) then
             open(unit=17, file='den.don')
       else if(n_read .eq. 2) then           
          open(unit=14, file='e0_nxlo.don')
          nxdata = n
       end if
           
       if(n_read .eq. 0) then
          do i=1,n
             read(14,*) xkf, ydata(i), zdata(i)
             xdata(i)= (2.d0/3.d0)*xkf**3/pi2
             easym(i) = zdata(i)-ydata(i)
          end do
          n2 = n-1
       else if(n_read .eq. 1) then
          do i=1,n_0
             read(14,*) xkfs, ydata(i)
             xdatas(i) = (2.d0/3.d0)*xkfs**3/pi2
          end do 
          do i=1,n_1
             read(15,*) xkfn, zdata(i)
             xdatan(i) = (1.d0/3.d0)*xkfn**3/pi2
          end do
          if(n .gt. 3) then
             do i = 1,n
                read(17,*) xdata(i) 
             end do
             n2 = n-1
          end if
       else if(n_read .eq. 2) then 
          do i=1,n
             read(14,*) xkf, ydata(i)
             xdata(i)= (2.d0/3.d0)*xkf**3/pi2
             easym(i) = ydata(i)
          end do 
          n2 = n-1
       end if

       if(mic .eq. 0) then 
          if(n_read .eq. 0) then
             do i=1,n 
                ydata(i) = e0_val(xdata(i))
          else if(n_read .eq. 1) then
             do i=1,n_0
                ydata(i) = e0_val(xdatas(i))
             end do
          else if(n_read .eq. 2) then 
             do i=1,n
                ydata(i) = e0_val(xdata(i))
             end do
        end if

c       set up EoS interpolation
       if(n_read .eq. 0) then
          call dcsakm(n,xdata,ydata,breaky,cscoefy)
          call dcsakm(n,xdata,zdata,breakz,cscoefz)
          call dcsakm(n,xdata,easym,breaks,cscoefs)
       else if(n_read .eq. 1) then
          call dcsakm(n_1,xdatan,zdata,breakz,cscoefz)
          call dcsakm(n_0,xdatas,ydata,breaky,cscoefy)
          if(n .gt. 3) then
             do i=1,n
                e0temp = dscval(xdata(i),n_1-1,breaky,cscoefy) 
                e1temp = dscval(xdata(i),n_0-1,breakz,cscoefz) 
                easym(i) = e1temp-e0temp
             end do
             call dcsakm(n,xdata,easym,breaks,cscoefs)
          else
             do i=1,n_0
                e1temp = dscval(xdatas(i),n_1-1,breakz,cscoefz) 
                easym(i) = e1temp-ydata(i) 
             end do
             call dcsakm(n_0,xdatas,easym,breaks,cscoefs)
          end if
       else if(n_read .eq. 2) then 
          call dcsakm(n, xdata, ydata, breaky, cscoefy)
          call dcsakm(n,xdata,easym,breaks,cscoefs)
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
                      easym(75),breaks(75),cscoefs(4,75),
                      den(75),breaka(75),cscoefa(4,75),
                      breakd(100), coeffd(4,100),
                      breakp0(100), coeffp0(4,100),
                      breakp1(100), coeffp1(4,100)

       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       common/readpar/n_read
       common/factor/pi,pi2

       common/pariso/nrho_ref, rho1, rho_ref(100)

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
          if(n .gt. 3):
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
          e01 = dscval(rho1,n2,breaky,cscoefy)
          e02 = dscval(rho2,n2,breaky,cscoefy)

          e1o = dcsval(rho0,n2,breakz,cscoefz)
          e11 = dcsval(rho1,n2,breakz,cscoefz)
          e12 = dscval(rho2,n2,breakz,cscoefz)

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

       else if(n_read .eq. 1)
          if(n .gt. 3) then
             rho1 = 0.1d0
             rho0 = dcsval(0.d0,n2,breakd,coeffd)
             rho2 = 2.d0*rho0

             e0o = dcsval(rho0,n_0-1,breaky,cscoefy)
             e01 = dscval(rho1,n_0-1,breaky,cscoefy)
             e02 = dscval(rho2,n_0-1,breaky,cscoefy)

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
             e01 = dscval(rho1,n_0-1,breaky,cscoefy)
             e02 = dscval(rho2,n_0-1,breaky,cscoefy)

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
          e01 = dscval(rho1,n2,breaky,cscoefy)
          e02 = dscval(rho2,n2,breaky,cscoefy)

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
          write(919,2023) bigL, bigK, bigKR, bigK0
          write(919,*) " "
          write(919,*) " "
       else
          write(919,*) "Iso-values: Isovector and Isoscalar values" 
          write(919,*) " "
          write(919,*) "  Rho0   Rho1   Rho2"
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
2021   format(2x,F7.4,2x,F7.4,2x,F7.4)
2022   format(2x,F8.4,2x,F8.4,2x,F8.4,2x,F8.4)
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

       if(nprint .eq. 0) then

       else
          write(777,*) '   den      ea0       ea2       ea4       ea6
     1ea8       ea1'
          do i=1,n
             write(777,1414) den(i), ea(1,i), ea(2,i),
     1                    ea(3,i), ea(4,i), ea(5,i), ea(6,i)
          end do
       end if

1414   format(2x,F8.4,2x,F8.4,2x,F8.4,2x,F8.4,2x,F8.4,
     1        2x,F8.4,2x,F8.4)

       end subroutine

