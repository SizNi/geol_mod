  MODULE shock2com
  PARAMETER (nx=40,ny=40,nskv=3)
  real a(nskv)/nskv*-10./, a1(nskv)
  integer nxskv(nskv)/20,30,25/ ,nyskv(nskv)/20,15,20/,nxs/20/,nys/27/
  real dt,dx(nx),dy(ny)
  integer nstep
  DATA dx /nx*10./ ,dy/ny*10./
  DATA dt /2/
  data nstep/400/

  END MODULE shock2com
