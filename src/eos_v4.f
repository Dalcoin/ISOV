c   EOS fortran Routines and Functions: Version 5.0 
c   Modified by: Dalcoin

c---------------------------------------------------------------------------------------------------
c                                      Initalization Routine                                       |
c---------------------------------------------------------------------------------------------------

c   The "init" subroutine intializes splines used to 
c   compute Binding Energy and nuclei parameters 

       subroutine init(n1_, n2_, n3_, x1_, x2_, ta_, tz_) 
       implicit real*8 (a-h,o-z)                     
       common/paspoi/pas(200),poi(200),x(200),w(200) 
       common/binding/totbe,binde1,binde2,binde3
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm, 
     1                 breakz(75),cscoefz(4,75),       
     2                 breaky(75),cscoefy(4,75),       
     4                 xdatas(100),xdatan(100)
       common/abc/xnorm 
       common/charge/chr  
       common/main/fint1,fint2,fint3       
       common/azn/ta, tz, tn
       common/setup/n1, n2, n3, x1, x2
       common/factor/pi,pi2
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       common/readpar/n_read 
 
       pi=3.141592654d0 
       pi2=pi*pi
 
c    number of integration points                             
       n1 = n1_
       n2 = n2_
       n3 = n3_
c     integration limits 
       x1 = x1_
       x2 = x2_
c     characteristics of the nucleus 
       ta = ta_
       tz = tz_
       tn = ta-tz 

c       open(unit=000,file='dump.don')
       open(unit=515,file='par.don')
       read(515,*) n, n_den, n_read, n_0, n_1,
     1             mic,isnm,isym_emp,k0,rho0,fff

       if(n_read .eq. 0) then
          open(unit=14,file='ex_nxlo.don')
          nxdata = n
          nxnm = n 
       else if(n_read .eq. 1) then 
          open(unit=14, file='e0_nxlo.don') 
          open(unit=15, file='e1_nxlo.don')
          nxdata = n_0
          nxnm = n_1   
       else if(n_read .eq. 2) then           
          open(unit=14, file='e0_nxlo.don')
          nxdata = n
       end if
           
       if(n_read .eq. 0) then
          do i=1,n
             read(14,*) xkf, ydata(i), zdata(i)
             xdata(i)= (2.d0/3.d0)*xkf**3/pi2
          end do
        else if(n_read .eq. 1) then
          do i=1,n_0
             read(14,*) xkfs, ydata(i)
             xdatas(i) = (2.d0/3.d0)*xkfs**3/pi2
          end do 
          do i=1,n_1
             read(15,*) xkfn, zdata(i)
             xdatan(i) = (1.d0/3.d0)*xkfn**3/pi2
          end do
        else if(n_read .eq. 2) then 
          do i=1,n
             read(14,*) xkf, ydata(i)
             xdata(i)= (2.d0/3.d0)*xkf**3/pi2
          end do 
       end if
           
c       set up interpolation
       if(n_read .eq. 0) then
          call dcsakm(n,xdata,zdata,breakz,cscoefz)
          call dcsakm(n,xdata,ydata,breaky,cscoefy)
       else if(n_read .eq. 1) then
          call dcsakm(n_1,xdatan,zdata,breakz,cscoefz)
          call dcsakm(n_0,xdatas,ydata,breaky,cscoefy)
       else if(n_read .eq. 2) then 
          call dcsakm(n, xdata, ydata, breaky, cscoefy)
       end if
                 
       return
       end
             
c---------------------------------------------------------------------------------------------------
c                            Total Energy Per Particle Calculuations                               |
c---------------------------------------------------------------------------------------------------
c     Main Function: Calculates the energy per particle for given rho() parameters      
       function energy(rp, cp, wp, rn, cn, wn)
       implicit real*8 (a-h,o-z)                     
       common/paspoi/pas(200),poi(200),x(200),w(200) 
       common/binding/totbe,binde1,binde2,binde3
       common/abc/xnorm 
       common/charge/chr  
       common/main/fint1,fint2,fint3         
       common/azn/ta, tz, tn
       common/setup/n1, n2, n3, x1, x2
       common/factor/pi,pi2 
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       common/readpar/n_read 
       
c       open(000,file='dump.don')

       dt = 0.d0

      if(n_read .eq. 2) then 
          rp = rn
          cp = cn 
          wp = wn
      end if

c     normalize the proton function
       if(n_den .EQ. 2 .OR. n_den .EQ. 4) then
          call xnormalize(pi,rp,cp,tz,dt)
       else if(n_den .EQ. 3) then
          call xnormalize(pi,rp,cp,tz,wp)
       end if
       ap=xnorm
               
c     normalize the neutron function
       if(n_den .EQ. 2 .OR. n_den .EQ. 4) then
          call xnormalize(pi,rn,cn,tn,dt)
       else if(n_den .EQ. 3) then
          call xnormalize(pi,rn,cn,tn,wn)
       end if
       an=xnorm 
       
       if(n_den .EQ. 2 .OR. n_den .EQ. 4) then
          call eos(n1,pi,x1,x2,ap,rp,cp,dt,an,rn,cn,dt)
          call be2(n2,pi,x1,x2,ap,rp,cp,dt,an,rn,cn,dt)
          call be3(n3,pi,x1,x2,ap,rp,cp,dt)
       else if(n_den .EQ. 3) then                      
          call eos(n1,pi,x1,x2,ap,rp,cp,wp,an,rn,cn,wn)               
          call be2(n2,pi,x1,x2,ap,rp,cp,wp,an,rn,cn,wn)               
          call be3(n3,pi,x1,x2,ap,rp,cp,wp)      
       end if    
       energy = (binde1+binde2+binde3)/ta
       
c       write(000,*) ap, an, binde1, binde2, binde3
                
       end 

c---------------------------------------------------------------------------------------------------
c                                 Normalization Routines                                           |
c---------------------------------------------------------------------------------------------------
       subroutine xnormalize(pi,b,c,xg,wi) 
c 
       implicit real*8 (a-h,o-z)                     
       common/paspoi/pas(200),poi(200),x(200),w(200) 
       common/abc/xnorm 
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
ca
c       open(000,file='dump.don')
       
       sum=0.d0
       x1=0.d0
       x2=20.d0 
       xinf=0.d0
       nnorm=90    
       xnorm=1.d0 

       call lgauss(nnorm)
       call papoi(x1,x2,1,nnorm,xinf,1)

       sum=0.d0 
       do 10 i=1,nnorm
          r=pas(i)
          ww=poi(i)
          if(n_den .EQ. 2) then
             funct=rho(r,xnorm,b,c)*r**2*ww
          else if(n_den .EQ. 3) then 
             funct=rho_3pf(r,xnorm,b,c,wi)*r**2*ww
          else if(n_den .EQ. 4) then
             funct=rho_fy(r,xnorm,b,c,xg)*r**2*ww
          end if    
10     sum=sum+funct
       sum=sum*4.d0*pi
       xnorm=xg/sum
       return
       end 


c---------------------------------------------------------------------------------------------------


c---------------------------------------------------------------------------------------------------
c                                         Density Functions                                        |
c---------------------------------------------------------------------------------------------------


       function rho(xr,xa,xb,xc)
       implicit real*8 (a-h,o-z)                     
          rho=xa/(1.d0+dexp((xr-xb)/xc))
       end 


       function rho_3pf(xr,xa,xb,xc,xw)
       implicit real*8 (a-h,o-z)
          rho_3pf=(1.d0+((xr**2)*dabs(xw))/(xb**2))*
     1        (xa/(1.d0+dexp((xr-xb)/xc)))
       end 


       function rho_fy(xr,xa,xb,xc,xg)
       implicit real*8(a-h,o-z)
       cof = (3.d0*xg)/(4.d0*(3.14159d0)*xb*xb*xb)
       erterm = (xc/xr)*dexp(-(xr/xc))
       ebrterm = (xc/xr)*dexp(-(xb/xc))
       sh = dsinh(xb/xc)
       ch = dcosh(xb/xc)
       if(xr .lt. xb) then
          rho_fy = cof*(1.d0-ebrterm*(1.d0+(xb/xc))*dsinh(xr/xc))
       else if(xr .gt. xb) then
          rho_fy = cof*erterm*((xb/xc)*ch - sh)
       end if
       end   

c-------------------------------------------------
c               Density Derivative               |
c-------------------------------------------------

       function devrho(xr,xa,xb,xc)
       implicit real*8 (a-h,o-z)       
          devrho=(-(xa/xc)*dexp((xr-xb)/xc))/
     1 ((1.d0+dexp((xr-xb)/xc))**2)    
       end 


       function devrho_3pf(xr,xa,xb,xc,xw)
       implicit real*8 (a-h,o-z)
          devrho_3pf = devrho(xr,xa,xb,xc) + 
     1    2.d0*(dabs(xw)/xb**2)*xr*rho(xr,xa,xb,xc)+
     1    (dabs(xw)/xb**2)*(xr**2)*devrho(xr,xa,xb,xc)
       end


       function devrho_fy(xr,xa,xb,xc,xg)
       implicit real*8(a-h,o-z)
       cof = (3.d0*xg)/(4.d0*(3.14159d0)*xb**3)
       erterm = (xc/xr)*dexp(-(xr/xc))
       ebrterm = (xc/xr)*dexp(-(xb/xc))
       sh = dsinh(xb/xc)
       ch = dcosh(xb/xc)
       shr = dsinh(xr/xc)
       chr = dcosh(xr/xc)
       if(xr .lt. xb) then
          devrho_fy = -cof*(1.d0+(xb/xc))*dexp(-xb/xc)*
     1                ((chr/xr)-(xc*shr/xr**2))
       else if(xr .gt. xb) then
          devrho_fy = -cof*((xb/xc)*ch - sh)*
     1                ((erterm/xr)+(erterm/xc))
       end if
       end


c---------------------------------------------------------------------------------------------------
c                                        SEMF Components                                           |
c---------------------------------------------------------------------------------------------------

       subroutine rho_from_coefs(r,ap,rp,cp,wp,an,rn,cn,wn)
       implicit real*8(a-h,o-z)
       common/rhoeval/rhoneu,rhopro,rhotot,alphapar
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff       
       common/azn/ta, tz, tn

       if(n_den .EQ. 2) then
          rhoneu = rho(r,an,rn,cn)
          rhopro = rho(r,ap,rp,cp)          
       else if(n_den .EQ. 3) then
          rhoneu = rho_3pf(r,an,rn,cn,wn) 
          rhopro = rho_3pf(r,ap,rp,cp,wp)
       else if(n_den .EQ. 4) then
          rhoneu = rho_fy(r,an,rn,cn,tn) 
          rhopro = rho_fy(r,ap,rp,cp,tz)
       end if        

       rhotot = rhoneu + rhopro
       alphapar = (rhoneu-rhopro)/rhotot
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
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff

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


       function ea(rho, alp)
       implicit real*8(a-h,o-z)
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm, 
     1                 breakz(75),cscoefz(4,75),       
     2                 breaky(75),cscoefy(4,75),  
     4                 xdatas(100),xdatan(100)
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       common/readpar/n_read 

c      calculates the energy-per-particle from a given density and alpha:
c      alp = (rho_n-rho_p)/(rho_n+rho_p)
c      ea = e0 + alp*alp*(esym)
c      esym = e1 - e0

       alp2 = alp*alp

       e0 = e0_val(rho)             

       if(n_read .eq. 2) then 
          pt = e0
          goto 4295
       end if 

       e1 = e1_val(rho)

c    Calculating the Energy per Particle due to Nuclear Forces

       if(isym_emp.eq.0) then
          pt=e0+(alp2)*(e1-e0) 
       else 
          pt=e0+(alp2)*esym_ph(rho, 0.72d0)      
       end if        

4295   continue

       ea = pt 
       end 

                 

c-------------------------------------------------
c           Volume Nuclear Energy Term           |  
c-------------------------------------------------

c      This subroutine calculates the energy as a function of 
c      density and the symmetric energy parameter.

       subroutine eos(m,pi,x1,x2,a,b,c,wt,a2,b2,c2,wt2)             

       implicit real*8 (a-h,o-z)                     

       common/paspoi/pas(200),poi(200),x(200),w(200)
       common/binding/totbe,binde1,binde2,binde3
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm, 
     1                 breakz(75),cscoefz(4,75),       
     2                 breaky(75),cscoefy(4,75),  
     4                 xdatas(100),xdatan(100)
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       common/azn/ta, tz, tn
       dimension xx(100)            
        
c  Generates the interpolated neutron matter EoS
c  parametrization of empirical EoS for symmmetric nuclear matter
           
       call lgauss(m)
       call papoi(x1,x2,1,m,0.d0,1)        
       sum=0.d0
       sum2=0.d0
       do 20 i=1,m
          r=pas(i)
          ww=poi(i)
          if(n_den .EQ. 2) then
             datapt=rho(r,a,b,c)+rho(r,a2,b2,c2)                      
             alp=(rho(r,a2,b2,c2)-rho(r,a,b,c))/datapt
          else if(n_den .EQ. 3) then
             datapt=rho_3pf(r,a,b,c,wt)+rho_3pf(r,a2,b2,c2,wt2)
             alp=(rho_3pf(r,a2,b2,c2,wt2)-rho_3pf(r,a,b,c,wt))/datapt
          else if(n_den .EQ. 4) then
             datapt=rho_fy(r,a,b,c,tz)+rho_fy(r,a2,b2,c2,tn)
             alp=(rho_fy(r,a2,b2,c2,tn)-rho_fy(r,a,b,c,tz))/datapt
          end if
                      
          pt=ea(datapt,alp)*datapt*r*r*ww
          sum=sum+pt
       
 20    continue 
        
       finalint=sum*4.d0*pi
       binde1=finalint
       return
       end 


c---------------------------------------------------------------------------------------------------

c-------------------------------------------------
c           Surface Nuclear Energy Term          |  
c-------------------------------------------------


       subroutine be2(nn,pi,x1,x2,a,b,c,wt,a2,b2,c2,wt2)  

       implicit real*8 (a-h,o-z)                     
       common/paspoi/pas(200),poi(200),x(200),w(200) 
       common/binding/totbe,binde1,binde2,binde3
       common/azn/ta, tz, tn
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       
       beta=1.d0     
c       fff = 65.d0
      
       n2=nn-1 
       call lgauss(nn)
       call papoi(x1,x2,1,nn,0.d0,1)   
            
       sum=0.d0
       do 20 i=1,nn 
          r=pas(i)
          ww=poi(i)
          if(n_den .EQ. 2) then
             funct1=devrho(r,a,b,c)
             funct2=devrho(r,a2,b2,c2)
          else if(n_den .EQ. 3) then
             funct1=devrho_3pf(r,a,b,c,wt)
             funct2=devrho_3pf(r,a2,b2,c2,wt2) 
          else if(n_den .EQ. 4) then
             funct1=devrho_fy(r,a,b,c,tz)
             funct2=devrho_fy(r,a2,b2,c2,tn)
          end if
          funct=funct1+funct2 
          funct=funct**2 
          funct=funct*fff*r**2*ww                                  
          sum=sum+funct
  20   continue 
       
       binde2=sum*4.d0*pi
       return
       end 
       
       
c---------------------------------------------------------------------------------------------------

c-------------------------------------------------
c              Coulomb Energy Term               |
c-------------------------------------------------


       subroutine be3(n,pi,x1,x2,a,b,c,wt)  
       implicit real*8 (a-h,o-z)                     
       common/paspoi/pas(200),poi(200),x(200),w(200) 
       common/binding/totbe,binde1,binde2,binde3
       common/azn/ta, tz, tn
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       dimension rp(200),wrp(200)       
c      
       n1=n
       n2=n
       call lgauss(n)
       call papoi(x1,x2,1,n,0.d0,1)        
       
       do 1 i=1,n 
          rp(i)=pas(i)
          wrp(i)=poi(i)
 1     continue 
       
       call lgauss(n)
       sum=0.d0
       
       do 20 j=1,n  
          xlow=0.d0
          xup=rp(j)
          call papoi(xlow,xup,1,n,0.d0,1)
          sum2=0.d0
          do 10 i=1,n
             r=pas(i)
             ww=poi(i)
c            internal integral
             if(n_den .EQ. 2) then
                funct=rho(r,a,b,c)*r**2.d0*ww
             else if(n_den .EQ. 3) then
                funct=rho_3pf(r,a,b,c,wt)*r**2.d0*ww
             else if(n_den .EQ. 4) then
                funct=rho_fy(r,a,b,c,tz)*r**2.d0*ww
             end if
             sum2=sum2+funct
 10       continue 
c     external integral
          if(n_den .EQ. 2) then
             functex=rp(j)*rho(rp(j),a,b,c)*sum2*wrp(j)
          else if(n_den .EQ. 3) then
             functex=rp(j)*rho_3pf(rp(j),a,b,c,wt)*sum2*wrp(j)
          else if(n_den .EQ. 4) then
             functex=rp(j)*rho_fy(rp(j),a,b,c,tz)*sum2*wrp(j)
          end if
          sum=sum+functex
 20    continue
       
       binde3=1.44d0*sum*(4.d0*pi)**2
       return
       end
c---------------------------------------------------------------------------------------------------

c---------------------------------------------------------------------------------------------------
c                            Atomic Parameters Calculations                                        |  
c---------------------------------------------------------------------------------------------------

c-------------------------------------------------
c         Charge Radius (Root Mean Squared)      |
c-------------------------------------------------
       subroutine chrms(a1,b1,c1,w1,pi,ttz,n)
       implicit real*8(a-h,o-z)
       common/paspoi/pas(200),poi(200),xfs(200),wfs(200)
       common/charge/chr 
       common/azn/ta, tz, tn
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff

       a=0.70 
c      a=0.87*dsqrt(2.d0/3.d0)
       x1=0.d0
       x2=20.d0 
       call lgauss(n)
       call papoi(x1,x2,1,n,xinf,1)

       sum2=0.d0
       do 106 j=1,n
          r=pas(j)
          ww=poi(j)
          fact3=dexp(-(r/a)**2.d0)
          sum1=0.d0
          do 105 i=1,n
             r1=pas(i)
             ww1=poi(i)
             fact1=dexp(-(r1/a)**2.d0)
             fact2=dsinh(2.d0*r*r1/(a**2.d0))
             if(fact2.gt.1.0d300) then
                funct1=0.d0
             else
                if(n_den .EQ. 2) then
                   funct1=r1*ww1*fact1*rho(r1,a1,b1,c1)*
     1             fact2*fact3/r
                else if(n_den .EQ. 3) then
                   funct1=r1*ww1*fact1*rho_3pf(r1,a1,b1,c1,w1)*
     1             fact2*fact3/r
                else if(n_den .EQ. 4) then
                   funct1=r1*ww1*fact1*rho_fy(r1,a1,b1,c1,tz)*
     1             fact2*fact3/r
                end if
             end if 
             sum1=sum1+funct1
  105     continue
          dinte=2.d0*sum1/(a*dsqrt(pi))
          funct2=4.d0*pi*r**4.d0*ww*dinte
          sum2=sum2+funct2
 106   continue 
       chr=dsqrt(sum2/ttz)
       end 


c-------------------------------------------------
c         Root Mean Squared Routine              |
c-------------------------------------------------
       subroutine rms(a1,b1,c1,w1,a2,b2,c2,w2,pi,tz,tn,ta,n)
       implicit real*8(a-h,o-z)
       common/paspoi/pas(200),poi(200),xfs(200),wfs(200)
       common/main/fint1,fint2,fint3
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
  
       sum1=0.d0
       sum2=0.d0
       sum3=0.d0
       sum4=0.d0 
       x1=0.d0
       x2=20.d0
 
       call lgauss(n)
       call papoi(x1,x2,1,n,xinf,1)
c
       do 10 i=1,n
          r=pas(i)
          ww=poi(i)
          if(n_den .EQ. 2) then
             funct1=rho(r,a1,b1,c1)
             funct2=rho(r,a2,b2,c2)
             funct3=rho(r,a1,b1,c1) + rho(r,a2,b2,c2)
          else if(n_den .EQ. 3) then
             funct1=rho_3pf(r,a1,b1,c1,w1)
             funct2=rho_3pf(r,a2,b2,c2,w2)
             funct3=rho_3pf(r,a1,b1,c1,w1) + rho_3pf(r,a2,b2,c2,w2)
          else if(n_den .EQ. 4) then
             funct1=rho_fy(r,a1,b1,c1,tz)
             funct2=rho_fy(r,a2,b2,c2,tn)
             funct3=rho_fy(r,a1,b1,c1,tz) + rho_fy(r,a2,b2,c2,tn)
          end if
          funct1=funct1*r**4.d0
          funct2=funct2*r**4.d0
          funct3=funct3*r**4.d0
          sum1=sum1+funct1*ww
          sum2=sum2+funct2*ww
          sum3=sum3+funct3*ww
  10   continue

       const1=(4.d0*pi)/tz
       const2=(4.d0*pi)/tn
       const3=(4.d0*pi)/ta
       fint1=dsqrt(sum1*const1)
       fint2=dsqrt(sum2*const2)
       fint3=dsqrt(sum3*const3)
       end 

c------------------------------------------------------
c         Symmetry Energy Coefficient Routine         |
c------------------------------------------------------
       subroutine sym_eng_coef(ap,rp,cp,wp,an,rn,cn,wn)
       implicit real*8 (a-h, o-z)
       common/paspoi/pas(200),poi(200),x(200),w(200)
       common/maineos/xdata(75),zdata(75),nxdata,
     3                 xsnm(75), ydata(75),nxnm,
     1                 breakz(75),cscoefz(4,75),
     2                 breaky(75),cscoefy(4,75),
     4                 xdatas(100),xdatan(100)
       common/azn/ta, tz, tn
       common/setup/n1, n2, n3, x1, x2
       common/factor/pi,pi2
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff
       common/esymc/esym_coef
       common/readpar/n_read

       nrep      =  90
       down_lim  =  0.d0
       upper_lim =  20.d0          

       sum=0.d0

       if(tn .ne. tz .and. n_read .ne. 2) then
          coef_int = ta/(tn-tz)**2
       else 
          coef_int = 0.d0
          go to 5543
       end if

       call lgauss(nrep)
       call papoi(down_lim,upper_lim,1,nrep,1.d0,1)

       do i =1,nrep

          dr = pas(i)
          ww = poi(i)

          if(n_den .EQ. 2) then
             rho_t = rho(dr,an,rn,cn)+rho(dr,ap,rp,cp)
             delt = (rho(dr,an,rn,cn)-rho(dr,ap,rp,cp))/rho_t
          else if(n_den .EQ. 3) then
             rho_t = rho_3pf(dr,an,rn,cn,wn)+rho_3pf(dr,ap,rp,cp,wp)
             delt = (rho_3pf(dr,an,rn,cn,wn)- 
     1               rho_3pf(dr,ap,rp,cp,wp))/rho_t
          else if(n_den .EQ. 4) then
             rho_t = rho_fy(dr,an,rn,cn,tn)+rho_fy(dr,ap,rp,cp,tz)
             delt = (rho_fy(dr,an,rn,cn,tn)-
     1               rho_fy(dr,ap,rp,cp,tz))/rho_t
          end if              
                      
          e0_eval = e0_val(rho_t)
          e1_eval = e1_val(rho_t)
              
          if(isym_emp.eq.0) then
             pt=(delt*delt)*(e1_eval-e0_eval) 
          else 
             pt=(delt*delt)*esym_ph(rho_t,0.72d0)    
          end if     
          
          eval = rho_t*pt*dr*dr*ww
          sum = sum + eval
       end do

5543   continue 

       esym_coef = sum*coef_int*4.d0*pi
       return 
       end


c---------------------------------------------------------------------------------------------------

       subroutine form_fac(qf,ac,rc,dc,wc,pi,tz,n)
       implicit real*8(a-h,o-z) 
       common/paspoi/pas(200),poi(200),xfs(200),wfs(200)
       common/form_pars/ff,ff2,ff2_log
       common/parz/n_den,mic,isnm,isym_emp,k0,rho0,fff

       xinf = 0.d0
       x1 = 0.d0
       x2 = 15.d0

       call lgauss(n)
       call papoi(x1,x2,1,n,xinf,1)

       coef = 4.d0*pi/tz
       
       sum=0.d0
       do j=1,n
          r=pas(j)
          ww=poi(j)
          if(dabs(qf*r) .LT. 0.0000001) then
             xjo = 1.0d0
          else 
             xjo = dsin(qf*r)/(qf*r) 
          end if

          if(n_den .EQ. 2) then
             rhozi = rho(r,ac,rc,dc)
          else if(n_den .EQ. 3) then
             rhozi = rho_3pf(r,ac,rc,dc,wc)
          else if(n_den .EQ. 4) then
             rhozi = rho_fy(r,ac,rc,dc,tz)
          end if
          gran = rhozi*xjo*(r**2)*ww 
          sum = sum + gran
       end do
       ff = coef*sum       
       ff2 = ff*ff
       ff2_log = dlog10(ff2)
       end 

c---------------------------------------------------------------------------------------------------
c                            Numeric Integration Subroutines                                       |
c---------------------------------------------------------------------------------------------------

c-------------------------------------------------
c          Legendre-Gaussian Integration         |
c-------------------------------------------------
       subroutine lgauss(n)
       implicit real*8(a-h,o-z)
       dimension z(200),wz(200)
       common/paspoi/pas(200),poi(200),xfs(200),wfs(200)
       
       if(n-1) 1,2,3
 1        return
 2        z(1)=0.d0
          wz(1)=2.d0
          return
 3        r=dfloat(n)
       g=-1.d0
       
       do 147 i=1,n
          test=-2.d0
          ic=n+1-i
          if(ic.lt.i) go to 150
 4           s=g
             t=1.d0
             u=1.d0
             v=0.d0
          do 50 k=2,n
             a=dfloat(k)
             p=((2.d0*a-1.d0)*s*g-(a-1.d0)*t)/a
             dp=((2.d0*a-1.d0)*(s+g*u)-(a-1.d0)*v)/a
             v=u
             u=dp
             t=s
 50       s=p
          if(abs((test-g)/(test+g)).lt.0.5d-09) go to 100
             sum=0.d0
          if(i.eq.1) go to 52
             do 51 j=2,i
                sum=sum+1.d0/(g-xfs(j-1))
 51          continue
 52       test=g
          g=g-p/(dp-p*sum)
          go to 4
 100      xfs(ic)=-g
          xfs(i)=g
          wfs(i)=2.d0/(r*t*dp)
          wfs(ic)=wfs(i)
 147   g=g-r*t/((r+2.d0)*g*dp+r*v-2.d0*r*t*sum)
 150   do 160 i=1,n
          z(i)=xfs(i)
          wz(i)=wfs(i)
 160   continue
       return
       end
c-------------------------------------------------
c              Steps and Weights                 |
c-------------------------------------------------
       subroutine papoi(xi,xf,ni,nf ,xinf,k)
       implicit real*8(a-h,o-z)
       common/paspoi/pas(200),poi(200),tp(200),hp(200)

       coeff=1.d0           
       go to (10,20,30) k
 10       xs=(xi+xf)/2.d0
          xd=(xf-xi)/2.d0
          do 1 i=ni,nf
             pas(i)=xs+xd*tp(i)
 1           poi(i)=xd*hp(i)
          return
 20       do 2 i=ni,nf
             pas(i)=((1.d0+tp(i))/(1.d0-tp(i)))*coeff+xinf
             poi(i)=2.d0*hp(i)/((1.d0-tp(i))**2)
             poi(i)=poi(i)*coeff
c 2   write(15,*) pas(i),poi(i),i
  2       continue
          return
 30    do 3 i=ni,nf
          pas(i)=xi*(1.d0+tp(i))/(1.d0-tp(i))+xinf
          poi(i)=2.d0*xi*hp(i)/((1.d0-tp(i))**2)
 3     continue                       
       return
       end
c-------------------------------------------------
