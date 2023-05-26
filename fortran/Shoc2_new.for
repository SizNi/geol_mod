MODULE shock2com
  PARAMETER (nx=40, ny=40, nskv=3)
  real a(nskv) /nskv*-10./, a1(nskv)
  integer nxskv(nskv) /20, 30, 25/, nyskv(nskv) /20, 15, 20/
  real dt, dx(nx), dy(ny)
  integer nstep
  DATA dx /nx*10./, dy /ny*10./
  DATA dt /1/
  data nstep /200/

END MODULE shock2com

$debug
USE shock2com
INTEGER, PARAMETER :: nrand = 100
INTEGER, PARAMETER :: npar = 5
REAL u(nrand, npar)
REAL kf, igrad, kmin, kmax, imin, imax, alfamin, alfamax, mmin, mmax, m
REAL c [ALLOCATABLE] (:,:)
REAL cx [ALLOCATABLE] (:,:)
REAL vx [ALLOCATABLE] (:,:)
REAL cy [ALLOCATABLE] (:,:)
REAL vy [ALLOCATABLE] (:,:)
REAL c1 [ALLOCATABLE] (:)
REAL v1 [ALLOCATABLE] (:)
REAL c05 [ALLOCATABLE] (:)
REAL crez [ALLOCATABLE] (:,:)
REAL q [ALLOCATABLE] (:,:)

INTEGER*2 ierr
INTEGER*4 step
mmin = 5
mmax = 10
pormin = .2
pormax = .4
imin = .001
imax = .01
alfamin = 270
alfamax = 330.
kmin = 5
kmax = 20
ALLOCATE(c(nx, ny), STAT=ierr)
ALLOCATE(cx(nx, ny), STAT=ierr)
ALLOCATE(cy(nx, ny), STAT=ierr)
ALLOCATE(vx(nx, ny), STAT=ierr)
ALLOCATE(vy(nx, ny), STAT=ierr)
ALLOCATE(crez(nx, ny), STAT=ierr)
ALLOCATE(q(nx, ny), STAT=ierr)

crez = 0.
q = 0.
CALL rands_1(nrand, npar, u)
DO irand = 1, nrand
  igrad = imin + u(irand, 1) * (imax - imin)
  alfa = alfamin + u(irand, 2) * (alfamax - alfamin)
  m = mmin + u(irand, 3) * (mmax - mmin)
  kf = kmin + u(irand, 4) * (kmax - kmin)
  por = pormin + u(irand, 5) * (pormax - pormin)
  DO i = 1, nskv
    a1(i) = a(i) / (m * por)
  END DO
  DO i = 1, nx
    DO k = 1, ny
      vx(i, k) = -kf * COSD(alfa) * igrad / por
      c(i, k) = 0.
      vy(i, k) = -kf * SIND(alfa) * igrad / por
      cx(i, k) = 0.
      cy(i, k) = 0.
    END DO
  END DO
  CALL VEL(ny, nx, dx, dy, VX, VY, A1, NXskv, NYskv, NSKV)
  DO nsk = 1, nskv
    q(NXskv(nsk), NYskv(nsk)) = -a1(nsk)
  END DO
loop1: DO step = 1, nstep
  DO nsk = 1, nskv
    c(NXskv(nsk), NYskv(nsk)) = 1
  END DO
  ALLOCATE(c05(nx + 1), STAT=ierr)
  ALLOCATE(v1(nx + 1), STAT=ierr)
  ALLOCATE(c1(nx + 1), STAT=ierr)
loop2: DO k = 2, ny - 1
  DO i = 1, nx
    c1(i) = c(i, k)
    v1(i) = vx(i, k)
  END DO
  CALL shock1(c05, c1, v1, dx, dt, nx)
  DO i = 1, nx
    cx(i, k) = c05(i)
  END DO
END DO loop2
  DEALLOCATE(c05, v1, c1)
  ALLOCATE(c05(ny + 1), STAT=ierr)
  ALLOCATE(v1(ny + 1), STAT=ierr)
  ALLOCATE(c1(ny + 1), STAT=ierr)
loop3: DO i = 2, nx - 1
  DO k = 1, ny
    c1(k) = c(i, k)
    v1(k) = vy(i, k)
  END DO
  CALL shock1(c05, c1, v1, dy, dt, ny)
  DO k = 1, ny
    cy(i, k) = c05(k)
  END DO
END DO loop3
  DEALLOCATE(c05, v1, c1)
  DO k = 2, ny - 2
    DO i = 2, nx - 2
      c(i, k) = c(i, k) + dt / (dx(i) * dy(k)) * (dy(k) * (vx(i - 1, k) * cx(i - 1, k) - vx(i, k) * cx(i, k)) + dx(i) * (vy(i, k - 1) * cy(i, k - 1) - vy(i, k) * cy(i, k) + Q(i, k) * c(i, k)))
    END DO
  END DO
END DO loop1

DO i = 1, nx
  DO k = 1, ny
    IF (c(i, k) .GE. 0.5) THEN
      crez(i, k) = crez(i, k) + 1.
    END IF
  END DO
END DO
DO i = 1, nx - 1
  DO k = 1, ny - 1
    ! write (1,'(6g12.5)')i*10.-5.,400-k*10.+5., c(i,k),crez(i,k),vx(i,k),vy(i,k)
    WRITE (1, '(6g12.5)') i * 10. - 5., k * 10. - 5., c(i, k), crez(i, k), vx(i, k), vy(i, k)
  END DO
END DO
END
