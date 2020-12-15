c   ISO fortran Routines and Functions: Version 5.0 
c   Written by: Randy Millerson

       program isovalues
       implicit real*8(a-h,o-z)

       common/maineos/xdata(100),zdata(100),
     1                 xsnm(100), ydata(100),
     2                 breakz(100),cscoefz(4,100),
     3                 breaky(100),cscoefy(4,100),
     4                 xdatas(100),xdatan(100)
       common/mainiso/n,n0,n1,n_read,ndn_read,nkf_read,n2,n3,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100),
     6                breakps(100), coeffps(4,100)


       common/dvals/desym(100),de0(100),de1(100),
     1              prse0(100),prse1(100),prsesym(100)

       common/isovals/rho1,rho0,rho2,e0o,e01,e02,e1o,
     1                e11,e12,prs0o,prs01,prs02,prs1o,
     2                prs11,prs12,esym0,esym1,esym2,
     3                bigL,bigK,bigKR,bigK0

       common/paremp/mic,isnm,isym_emp,gam,xk0,rhosat

       common/parabeos/denarr(100),e0arr(100),esymarr(100),nt

       common/pheneos/gamma, nc

       open(unit=100,file='execpar.don')
       read(100,*) nrun, nprint

       call readEoS(nrun)

       if(nrun .eq. 1) then
          call getISO(0)
          call printISO(nprint)
       else if(nrun .eq. 2) then
          call parab(nprint)
       else if(nrun .eq. 3) then
          call phen_eos()
       end if

 9999  stop
       end program



c      Subroutine to read in EoS, run this first for the ISO routine
       subroutine readEoS(nrun)
c      creates a series of splines for the input nuclear EoS.
c      Splines created are den vs. energy-per-particle for both
c      symmetric and neutron matter as well as den vs. pressure

       implicit real*8(a-h,o-z)
       common/maineos/xdata(100),zdata(100),
     1                 xsnm(100), ydata(100),
     2                 breakz(100),cscoefz(4,100),
     3                 breaky(100),cscoefy(4,100),
     4                 xdatas(100),xdatan(100)
       common/mainiso/n,n0,n1,n_read,ndn_read,nkf_read,n2,n3,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100),
     6                breakps(100), coeffps(4,100)

       common/paremp/mic,isnm,isym_emp,gam,xk0,rhosat

       common/parabeos/denarr(100),e0arr(100),esymarr(100),nt

       common/factor/pi,pi2

       pi=3.141592654d0 
       pi2=pi*pi

c       open(unit=000,file='dump.don')



       open(unit=515,file='readpar.don')
       open(unit=616,file='phenpar.don')
       read(515,*) n_read, nkf_read, ndn_read, n, n0, n1
       read(616,*) mic, isnm, isym_emp, gam, xk0, rhosat

       if(nrun .eq. 3) then
           go to 300
       end if

       if(n_read .eq. 0) then
          n1 = n0
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

       if(mic .eq. 0) then
          do i=1,n0
             ydata(i) = e0_val(xdatas(i))
          end do
       end if

c       set up EoS interpolation
       if(n_read .eq. 0) then
          call dcsakm(n0,xdatas,ydata,breaky,cscoefy)
          call dcsakm(n0,xdatas,zdata,breakz,cscoefz)
          call dcsakm(n0,xdatas,easym,breaks,cscoefs)
       else if(n_read .eq. 1) then
          call dcsakm(n0,xdatas,ydata,breaky,cscoefy)
          call dcsakm(n1,xdatan,zdata,breakz,cscoefz)
          do i=1,n0
             e1temp = dcsval(xdatas(i),n1-1,breakz,cscoefz) 
             easym(i) = e1temp-ydata(i) 
          end do
          call dcsakm(n0,xdatas,easym,breaks,cscoefs)
       end if

300    continue
       if(n .gt. 0) then
          open(unit=17, file='den.don')
          do i=1,n
             read(17,*) xden
             if(ndn_read .eq. 1) then
                den(i)= (2.d0/3.d0)*xden*xden*xden/pi2
             else if(ndn_read .eq. 0) then
                den(i)= xden
             end if
          end do
       end if

       if(nrun .eq. 2) then
          if(n .gt. 0) then
             do i=1,n
                denarr(i) = den(i)
                e0arr(i) = dcsval(den(i),n-1,breaky,cscoefy)
                esymarr(i) = dcsval(den(i),n-1,breaks,cscoefs)
             end do
             nt = n
          else
             do i=1,n0
                denarr(i) = den(i)
                e0arr(i) = dcsval(den(i),n0-1,breaky,cscoefy)
                esymarr(i) = dcsval(den(i),n0-1,breaks,cscoefs)
             end do
             nt = n0
          end if
       end if

       return
       end



!      Routine to set up interpolation of the nuclear EoS
       subroutine getISO(nswitch)
       implicit real*8(a-h,o-z)

       common/maineos/xdata(100),zdata(100),
     1                 xsnm(100), ydata(100),
     2                 breakz(100),cscoefz(4,100),
     3                 breaky(100),cscoefy(4,100),
     4                 xdatas(100),xdatan(100)
       common/mainiso/n,n0,n1,n_read,ndn_read,nkf_read,n2,n3,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100),
     6                breakps(100), coeffps(4,100)

       common/dvals/desym(100),de0(100),de1(100),
     1              prse0(100),prse1(100),prsesym(100)

       common/isovals/rho1,rho0,rho2,e0o,e01,e02,e1o,
     1                e11,e12,prs0o,prs01,prs02,prs1o,
     2                prs11,prs12,esym0,esym1,esym2,
     3                bigL,bigK,bigKR,bigK0

       common/paremp/mic,isnm,isym_emp,gam,xk0,rhosat
       common/factor/pi,pi2

       nexit = 0
       if(nswitch .lt. 0 .or. nswitch .gt. 1) then 
           goto 9999
       else if(nswitch .eq. 0 .or. nswitch .eq. 1) then
           nexit = nswitch
       end if

c      Pressure & Iso-value interpolation
       if(n_read .eq. 0) then
          n2 = n0-1
          n3 = n2
          do i=1,n0
            desym(i) = dcsder(1,xdatas(i),n2,breaks,cscoefs)
            de0(i) = dcsder(1,xdatas(i),n2,breaky,cscoefy)
            de1(i) = dcsder(1,xdatas(i),n2,breakz,cscoefz)
            prse0(i) = xdatas(i)*xdatas(i)*de0(i)
            prse1(i) = xdatas(i)*xdatas(i)*de1(i)
            prsesym(i) = xdatas(i)*xdatas(i)*desym(i)
          end do
          call dcsakm(n0,de0,xdatas,breakd,coeffd)
          call dcsakm(n0,xdatas,prse0,breakp0,coeffp0)
          call dcsakm(n0,xdatas,prse1,breakp1,coeffp1)
          call dcsakm(n0,xdatas,prsesym,breakps,coeffps)
       else if(n_read .eq. 1) then
          n2 = n0-1
          n3 = n1-1
          do i=1,n0
             desym(i) = dcsder(1,xdatas(i),n2,breaks,cscoefs)
             de0(i) = dcsder(1,xdatas(i),n2,breaky,cscoefy)
             prse0(i) = xdatas(i)*xdatas(i)*de0(i)   
             prsesym(i) = xdatas(i)*xdatas(i)*desym(i)
          end do
          do i=1,n1
             de1(i) = dcsder(1,xdatan(i),n3,breakz,cscoefz)
             prse1(i) = xdatan(i)*xdatan(i)*de1(i)
          end do
          call dcsakm(n0,de0,xdatas,breakd,coeffd)
          call dcsakm(n0,xdatas,prse0,breakp0,coeffp0)
          call dcsakm(n1,xdatan,prse1,breakp1,coeffp1)
          call dcsakm(n0,xdatas,prsesym,breakps,coeffps)
       end if

       if(nexit .eq. 1) then 
           goto 9999
       end if

       rho1 = 0.1d0
       rho0 = dcsval(0.d0,n2,breakd,coeffd)
       rho2 = 2.d0*rho0

       e0o = dcsval(rho0,n2,breaky,cscoefy)
       e01 = dcsval(rho1,n2,breaky,cscoefy)
       e02 = dcsval(rho2,n2,breaky,cscoefy)

       e1o = dcsval(rho0,n3,breakz,cscoefz)
       e11 = dcsval(rho1,n3,breakz,cscoefz)
       e12 = dcsval(rho2,n3,breakz,cscoefz)

       prs0o = dcsval(rho0,n2,breakp0,coeffp0)
       prs01 = dcsval(rho1,n2,breakp0,coeffp0)
       prs02 = dcsval(rho2,n2,breakp0,coeffp0)

       prs1o = dcsval(rho0,n3,breakp1,coeffp1)
       prs11 = dcsval(rho1,n3,breakp1,coeffp1)
       prs12 = dcsval(rho2,n3,breakp1,coeffp1)

       esym0 = dcsval(rho0,n2,breaks,cscoefs)
       esym1 = dcsval(rho1,n2,breaks,cscoefs)
       esym2 = dcsval(rho2,n2,breaks,cscoefs)

       bigL = 3.d0*rho0*dcsder(1,rho0,n2,breaks,cscoefs) 
       bigK = 9.d0*rho0*rho0*dcsder(2,rho0,n2,breaks,cscoefs)
       bigKR= 9.d0*rho1*rho1*dcsder(2,rho1,n2,breaks,cscoefs)
       bigK0= 9.d0*rho0*rho0*dcsder(2,rho0,n2,breaky,cscoefy)

9999   return           
       end


       subroutine printISO(nprint)
       implicit real*8(a-h,o-z)

       common/maineos/xdata(100),zdata(100),
     1                 xsnm(100), ydata(100),
     2                 breakz(100),cscoefz(4,100),
     3                 breaky(100),cscoefy(4,100),
     4                 xdatas(100),xdatan(100)
       common/mainiso/n,n0,n1,n_read,ndn_read,nkf_read,n2,n3,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100),
     6                breakps(100), coeffps(4,100)

       common/dvals/desym(100),de0(100),de1(100),
     1              prse0(100),prse1(100),prsesym(100)

       common/isovals/rho1,rho0,rho2,e0o,e01,e02,e1o,
     1                e11,e12,prs0o,prs01,prs02,prs1o,
     2                prs11,prs12,esym0,esym1,esym2,
     3                bigL,bigK,bigKR,bigK0

       if(nprint .eq. 1 .or. nprint .eq. 3) then
          open(unit=818,file='eosvals.don')
          if(n .gt. 0) then
             do i=1,n
                dn = den(i)
                e0v = dcsval(dn,n2,breaky,cscoefy) 
                e1v = dcsval(dn,n3,breakz,cscoefz)
                esv = dcsval(dn,n2,breaks,cscoefs)
                p0v = dcsval(dn,n2,breakp0,coeffp0)
                p1v = dcsval(dn,n3,breakp1,coeffp1)
                psv = dcsval(dn,n2,breakps,coeffps)
                write(818,*) dn, e0v, e1v, esv, p0v, p1v, psv
             end do
          else
             do i=1,n0
                dn = xdatas(i)
                e0v = dcsval(dn,n2,breaky,cscoefy) 
                e1v = dcsval(dn,n3,breakz,cscoefz)
                esv = dcsval(dn,n2,breaks,cscoefs)
                p0v = dcsval(dn,n2,breakp0,coeffp0)
                p1v = dcsval(dn,n3,breakp1,coeffp1)
                psv = dcsval(dn,n2,breakps,coeffps)
                write(818,*) dn, e0v, e1v, esv, p0v, p1v, psv
             end do
          end if
       end if

       if(nprint .eq. 2 .or. nprint .eq. 3) then
          open(unit=919,file='isovals.don')
          write(919,*)  n0
          write(919,*)  rho0
          write(919,*)  rho1
          write(919,*)  rho2
          write(919,*)  e0o
          write(919,*)  e01
          write(919,*)  e02
          write(919,*)  e1o
          write(919,*)  e11
          write(919,*)  e12
          write(919,*)  esym0
          write(919,*)  esym1
          write(919,*)  esym2
          write(919,*)  prs0o
          write(919,*)  prs01
          write(919,*)  prs02
          write(919,*)  prs1o
          write(919,*)  prs11
          write(919,*)  prs12
          write(919,*)  bigL
          write(919,*)  bigK
          write(919,*)  bigKR
          write(919,*)  bigK0
       else
          continue
       end if

       return
       end


       subroutine parab(nval)
c      Generates between 3 and 21 equations of state
c      for infinite nuclear matter at varying 
c      densities but with increasing asymmetry ranging
c      from symmetric to pure neutron matter.
c      Arrays denarr, e0arr and esymarr must be set.

       implicit real*8(a-h,o-z)
       common/parabeos/denarr(100),e0arr(100),esymarr(100),nt
        
       dimension :: ea(21,100), alp(21)

       open(777,file='prbvals.don')

       pi=3.14159d0
       pi2 = pi*pi

       if(nval .lt. 2 .or. nval .gt. 21) then
           goto 4567
       end if

       do i=1,nval
          alp(i) = 0.d0 + (1.d0/((nval-1)*1.d0)) * (i-1)
       end do

       do j=1,nval
          do i=1,nt
             ea(j,i) = e0arr(i)+esymarr(i)*alp(j)*alp(j)
          end do
       end do

       do i=1,nt
          write(777,'(F12.6)',advance="no") denarr(i)
          do j=1,nval-1
              write(777,'(F12.4)',advance="no") ea(j,i)
          end do
          write(777,'(F12.4)') ea(nval,i)
       end do

4567   continue
       end subroutine


       subroutine phen_eos()
       implicit real*8(a-h,o-z)
       common/mainiso/n,n0,n1,n_read,ndn_read,nkf_read,n2,n3,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100),
     6                breakps(100), coeffps(4,100)

       common/paremp/mic,isnm,isym_emp,gam,xk0,rhosat

       pi=3.141592654d0 
       pi2=pi*pi

       open(unit=999,file='pheneos.don')

       write(999,*) "  den                phen"
       do i=1,n
          if(isnm .eq. 1) then
             ee = eafff(den(i))
          else if(isnm .eq. 2) then
             ee = earat(den(i))
          else if(isym_emp .eq. 1) then
             ee = esym_ph(den(i), gam)
          else
             ee = 0.d0
          end if
          write(999,*) den(i), ee
       end do
       return
       end


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
       common/paremp/mic,isnm,isym_emp,gam,xk0,rhosat

       pi=3.141592654d0 
       pi2=pi*pi
       
       rat=rho/rhosat
        
       fact=(3.d0*pi2/2.d0)**(2.d0/3.d0) 
       hbc=197.327d0
       hbc2=hbc**2
       xm=938.926d0 
       tfact=(3.d0*hbc2/10.d0/xm)
       totfact=fact*tfact
           
       alpha=-29.47-46.74*(xk0+44.21)/(xk0-166.11)
       beta=23.37*(xk0+254.53)/(xk0-166.11)       
       sigma=(xk0+44.21)/210.32                   
        
       earat = totfact*(rat)**(2.d0/3.d0) + (alpha/2.d0)*(rat)+
     1    (beta/(sigma + 1.d0))*(rat)**(sigma) 
        
       end 


       function e0_val(rho)
       implicit real*8(a-h,o-z)
       common/mainiso/n,n0,n1,n_read,ndn_read,nkf_read,n2,n3,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100),
     6                breakps(100), coeffps(4,100)
       common/maineos/xdata(100),zdata(100),
     1                 xsnm(100), ydata(100),
     2                 breakz(100),cscoefz(4,100),
     3                 breaky(100),cscoefy(4,100),
     4                 xdatas(100),xdatan(100)
       common/paremp/mic,isnm,isym_emp,gam,xk0,rhosat

c      Calculates the energy-per-particle for symmetric nuclear matter from a density

       nintv=n0-1

c      phenom_eos_section
       if(mic.eq.0) then 
       
          if(isnm.eq.1) then
             e0=eafff(rho) 
          else if(isnm .eq. 2) then
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
       common/mainiso/n,n0,n1,n_read,ndn_read,nkf_read,n2,n3,
     1                easym(100),breaks(100),cscoefs(4,100),
     2                den(100),breaka(100),cscoefa(4,100),
     3                breakd(100), coeffd(4,100),
     4                breakp0(100), coeffp0(4,100),
     5                breakp1(100), coeffp1(4,100),
     6                breakps(100), coeffps(4,100)
       common/maineos/xdata(100),zdata(100),
     1                 xsnm(100), ydata(100),
     2                 breakz(100),cscoefz(4,100),
     3                 breaky(100),cscoefy(4,100),
     4                 xdatas(100),xdatan(100)
       common/paremp/mic,isnm,isym_emp,xk0,rhosat

c      Calculates the energy-per-particle for neutron nuclear matter from a density
c      intialization (calling init) is assumed

       nintv2=n1-1 
       e1_val = dcsval(rho,nintv2,breakz,cscoefz)
       end   


       function esym_ph(rho, gam)
       implicit real*8(a-h,o-z)
       common/paremp/mic,isnm,isym_emp,xk0,rhosat
           
       rat=rho/rhosat
       esym_ph = 22.d0*rat**gam + 12.d0*rat**(2.d0/3.d0) 
       end 

