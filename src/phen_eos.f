       program phn_eos
       implicit real*8(a-h,o-z)

       dimension :: den(100)

c         phenom_eos_section

       open(unit=17, file='den.don')
       open(unit=515,file='par.don')
       open(unit=999,file='phn.don')

       read(515,*) n, n_den, n_read, n_0, n_1,
     1             mic,isnm,isym_emp,k0,rho0,fff

       do i=1,n
          read(17,*) den(i)
       end do

       do i=1,n 
          ee1 = eafff(den(i)) 
          ee2 = earat(den(i))
          esym = esym_ph(rho, 0.72)
          write(999,1010) den(i), ee1, ee2, ee3, pt
       end do      
1010   format(2x,F7.3,2x,F8.4,2x,F8.4,2x,F8.4,2x,F8.4)
       end