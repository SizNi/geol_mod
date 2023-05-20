subroutine Rands_1(nrand,npar,u)

     REAL  u(nrand,npar)
      CALL RANDOM_SEED()
      !CALL RANDOM_NUMBER(x)
      CALL RANDOM_NUMBER(u)
end subroutine Rands_1
