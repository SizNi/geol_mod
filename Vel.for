$     debug
      SUBROUTINE VEL(N1,N2,X,Y,VX,VY,A,NX,NY,NSKV)                      00000001
      DIMENSION X(n2),Y(n1),VX(n2,n1),VY(n2,n1),A(NSKV),
     #X1(100),Y1(nskv),NX(NSKV),NY(nskv)                                00000003
      DO 1 I=1,NSKV                                                     00000004
      X1(I   )=0                                                        00000005
      NXX=NX(I)
      DO 2 IX=2,NXX                                                     00000006
   2  X1(I   )=X1(I   )+(X(IX-1)+X(IX))/2 
       xc=x1(nskv)
      Y1(I   )=0                                                        00000008
      NYY=NY(I)
      DO 3 IY=2,NYY                                                     00000009
   3  Y1(I   )=Y1(I )  +(Y(IY-1)+Y(IY))/2  
       yc=y1(nskv)
   1  CONTINUE                                                          00000011
CCCC  X2=X(1)/2                                                           000000
      Y2=Y(1)/2                                                           000000
      DO 4 K=2,N1                                                       00000014
      X2=X(1)/2.
      DO 5 I=1,N2                                                       00000015
      Y3=Y2+Y(K)                                                        00000016
      DO 6 NS=1,NSKV                                                    00000017
      YB=Y3-Y1(NS)                                                      00000018
      YH=Y2-Y1(NS)                                                      00000019
      XX=X2-X1(NS  )                                                    00000020
      VX(i,K)=(-1)*A(NS  )*(ATAN (YB/XX)-ATAN (YH/XX))/Y(K)+VX(i,K)     00000021
C     V11=(-1.)*A(NS)
C     V12=ATAN (YB/XX)
C     V13=ATAN (YH/XX)
C     V14=(V12-V13)/Y(K)
C     VX(K,I)=V11*V14+VX(K,I)
   6  CONTINUE                                                          00000022
   5  if(i.lt.n2) X2=X2+X(I+1)                                                      00000023
   4  Y2=Y3                                                             00000024
      X2=X(1)/2                                                         00000025
      Y2=Y(1)/2                                                         00000026
      DO 7 I=2,N2                                                       00000027
      Y2=Y(1)/2
      DO 8 K=1,N1                                                       00000028
      X3=X2+X(I)                                                        00000029
      DO 9 NS=1,NSKV                                                      000000
      XP=X3-X1(NS)                                                      00000031
      XL=X2-X1(NS)                                                      00000032
      YY=Y2-Y1(NS  )                                                    00000033
      VY(i,K)=(-1)*A(NS  )*(ATAN (XP/YY)-ATAN (XL/YY))/X(I)+VY(i,K)      0000003
   9  CONTINUE                                                          00000035
   8  if(k.lt.n1) Y2=Y2+Y(K+1)                                                      00000036
   7  X2=X3                                                             00000037
      RETURN                                                            00000038
CCCC  DEBUG TRACE,INIT
      END                                                               00000039
