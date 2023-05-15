SUBROUTINE VEL(N1, N2, X, Y, VX, VY, A, NX, NY, NSKV)
   DIMENSION X(N2), Y(N1), VX(N2, N1), VY(N2, N1), A(NSKV), X1(100), Y1(NSKV), NX(NSKV), NY(NSKV)

   DO I = 1, NSKV
      X1(I) = 0
      NXX = NX(I)
      DO IX = 2, NXX
         X1(I) = X1(I) + (X(IX - 1) + X(IX)) / 2
      END DO
      xc = x1(nskv)
      Y1(I) = 0
      NYY = NY(I)
      DO IY = 2, NYY
         Y1(I) = Y1(I) + (Y(IY - 1) + Y(IY)) / 2
      END DO
      yc = y1(nskv)
   END DO

   X2 = X(1) / 2
   Y2 = Y(1) / 2
   DO K = 2, N1
      X2 = X(1) / 2.
      DO I = 1, N2
         Y3 = Y2 + Y(K)
         DO NS = 1, NSKV
            YB = Y3 - Y1(NS)
            YH = Y2 - Y1(NS)
            XX = X2 - X1(NS)
            VX(I, K) = (-1) * A(NS) * (ATAN(YB / XX) - ATAN(YH / XX)) / Y(K) + VX(I, K)
         END DO
         if (i < n2) X2 = X2 + X(I + 1)
      END DO
      Y2 = Y3
   END DO

   X2 = X(1) / 2
   Y2 = Y(1) / 2
   DO I = 2, N2
      Y2 = Y(1) / 2
      DO K = 1, N1
         X3 = X2 + X(I)
         DO NS = 1, NSKV
            XP = X3 - X1(NS)
            XL = X2 - X1(NS)
            YY = Y2 - Y1(NS)
            VY(I, K) = (-1) * A(NS) * (ATAN(XP / YY) - ATAN(XL / YY)) / X(I) + VY(I, K)
         END DO
         if (k < n1) Y2 = Y2 + Y(K + 1)
      END DO
      X2 = X3
   END DO

   RETURN
END
