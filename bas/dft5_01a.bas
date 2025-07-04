4 REM ******************************************
6 REM ** (DFT5.01A) GENERATE/ANALYZE WAVEFORM **
8 REM ******************************************
10 Q=32
12 PI=3.141592653589793#:P2=2*PI:K1=P2/Q:K2=1/PI
14 DIM C(2,Q), S(2,Q), KC(2,Q), KS(2,Q)
15 F9=Q/2
16 CLS:FOR J=0 TO Q:FOR I=1 TO 2: C(I,J)=0:S(I,J)=0:NEXT:NEXT
20 CLS:REM *   MAIN MENU   *
22 PRINT:PRINT:PRINT "     MAIN MENU":PRINT
24 PRINT " 1 = SIMILARITY THEOREM":PRINT
31 PRINT " 2 = EXIT":PRINT:PRINT
32 PRINT SPC(10);"MAKE SELECTION";
34 A$ = INKEY$:IF A$="" THEN 34
36 A=VAL(A$):ON A GOSUB 300,1000
38 GOTO 20
40 CLS:N=1:M=2:K5=Q:K6=-1:GOSUB 108
42 FOR J=0 TO Q:C(2,J)=0:S(2,J)=0:NEXT
44 GOSUB 200: REM - PERFORM DFT
46 GOSUB 140: REM - PRINT OUT FINAL VALUES
48 PRINT:INPUT "C/R TO CONTINUE";A$
50 RETURN
80 CLS:GOSUB 150: REM PRINT HEADING
81 FOR I=0 TO Q-1:C(1,I)=0:S(1,I)=0:NEXT
82 N=2:M=1:K5=1:K6=1
84 GOSUB 200:REM INVERSE TRANSFORM
86 GOSUB 140:REM PRINT OUTPUT
88 PRINT:INPUT "C/R TO CONTINUE"; A$
90 RETURN
100 REM ********************************************
101 REM *        PROGRAM SUBROUTINES               *
102 REM ********************************************
104 REM *       PRINT COLUMN HEADINGS              *
105 REM ********************************************
106 REM *      FREQUENCY DOMAIN HEADING            *
107 REM ********************************************
108 PRINT:PRINT :IF COR$="P" THEN 116
109 PRINT "FREQ   F(COS)   F(SIN)   FREQ   F(COS)   F(SIN)"
110 PRINT
111 RETURN
112 REM ********************************************
113 REM *        POLAR COORDINATES HEADING         *
114 REM ********************************************
116 PRINT "FREQ   F(MAG)   F(THETA)  FREQ   F(MAG)   F(THETA)"
118 RETURN
137 REM *******************************
138 REM *      PRINT OUTPUT           *
139 REM *******************************
140 IF COR$="P" AND M=2 THEN GOSUB 170
141 FOR Z=0 TO Q/2-1
142 PRINT USING "##_    ";Z;
144 PRINT USING "+###.#####_   ";C(M,Z),S(M,Z);
145 PRINT USING "##_   ";(Z+Q/2);
146 PRINT USING "+###.#####_   ";C(M,Z+Q/2),S(M,Z+Q/2)
147 NEXT Z
148 RETURN
150 REM *****************************************
152 REM *   PRINT TIME DOMAIN COLUMN HEADINGS   *
153 REM *****************************************
154 PRINT
156 PRINT "                  RECONSTRUCTION":PRINT
158 PRINT " T                       T":PRINT
160 RETURN
169 REM *************************************************
170 REM * CONVERT FROM RECTANGULAR TO POLAR COORDINATES *
171 REM *************************************************
172 FOR I=0 TO Q-1
174 MAG=SQR(C(M,I)^2+S(M,I)^2)
175 IF C(M,I)=0 THEN 190
176 ANGLE=180/PI*ATN(S(M,I)/C(M,I))
177 IF C(M,I)>0 THEN S(M,I)=ANGLE:GOTO 180
178 IF ANGLE>0 THEN S(M,I)=ANGLE-180
179 IF ANGLE<0 THEN S(M,I)=ANGLE+180
180 C(M,I)=MAG:NEXT
182 RETURN
190 IF S(M,I)=0 THEN 180 
191 IF S(M,I)>0 THEN S(M,I)=90: GOTO 180
192 S(M,I)=-90: GOTO 180
200 REM *****************************
202 REM *    TRANSFORM/RECONSTRUCT  *
204 REM *****************************
206 FOR J=0 TO Q-1:REM SOLVE EQNS FOR EACH FREQUENCY
208 FOR I=0 TO Q-1:REM MULTIPLY AND SUM EACH POINT
210 C(M,J)=C(M,J)+C(N,I)*COS(J*I*K1)-K6*S(N,I)*SIN(J*I*K1)
211 S(M,J)=S(M,J)+K6*C(N,I)*SIN(J*I*K1)+S(N,I)*COS(J*I*K1)
212 NEXT I
214 C(M,J)=C(M,J)/K5:S(M,J)=S(M,J)/K5:REM SCALE RESULTS
216 NEXT J
218 RETURN
220 REM *****************************
222 REM *      PLOT FUNCTIONS       *
224 REM *****************************
225 SFF=16:SFT=64
226 SCREEN 9,1,1,1:COLOR 9,1,1:CLS:YF=-1:YT=-1
228 LINE (0,5) - (0,155):LINE (0,160) - (0,310)
230 LINE (0,155) - (600,155):LINE (0,310)-(600,310)
232 GOSUB 266 :REM SET SCALE FACTORS
234 COLOR 15,1,1
236 FOR N=0 TO Q-1 : REM PLOT DATA
238 GOSUB 260 :REM CONVERT DATA TO PIXELS
240 LINE (X,Y) - (X,Y):LINE (X,Z) - (X,Z)
242 NEXT N
244 LOCATE 2,10:PRINT "FREQUENCY DOMAIN (MAG)"
246 LOCATE 14,12:PRINT "TIME DOMAIN"
248 LOCATE 24,1
250 INPUT "C/R TO CONTINUE": A$
252 SCREEN 0,0,0
254 RETURN
256 REM ****************************
257 REM * COMPUTE SCREEN LOCATIONS *
258 REM ****************************
260 Y=SQR(C(2,N)^2+S(2,N)^2):Y=155 - (YF*Y)
261 X=N*600/Q:Z=310-(YT*C(1,N))
262 RETURN
263 REM *******************************
264 REM *  SET & PRINT SCALE FACTORS  *
265 REM *******************************
266 YF=150/SFF:YT=150/SFT:LINE (0,5) - (5,5): LINE (0,80) - (5,80)
268 LINE (0,160) - (5,160):LINE (0,235) - (5,235)
270 LOCATE 1,2:PRINT SFF :LOCATE 6,2:PRINT SFF/2
272 LOCATE 12,2:PRINT SFT:LOCATE 17,2:PRINT SFT/2
274 RETURN
299 REM *****************************
300 CLS:REM *  SIMILARITY THEOREM   *
302 REM CLEAR ARRAYS
304 FOR I=0 TO Q-1:C(1,I)=0:S(1,I)=0
306 FOR J=1 TO 2:KC(J,I)=0:KS(J,I)=0:NEXT:NEXT
308 CLS:PRINT "WIDTH =";F9:REM DISPLAY CURRENT WIDTH
310 INPUT "WIDTH ";F9 :REM INPUT WIDTH
311 REM CHECK WIDTH LIMITS
312 IF F9>Q/2 THEN PRINT Q/2;" DATA POINTS MAXIMUM":F9=Q/2
314 IF F9<1 THEN PRINT "1 DATA POINTS MINIMUM":F9=1 
316 PRINT SPC(13);"SIMILARITY TEST - WIDTH =";F9
317 FOR I=Q/2-F9 TO Q/2+F9:REM GENERATE INPUT FUNCTION
318 C(1,I)=Q*(SIN(PI*(I-(Q/2-F9))/(2*F9)))^2
319 NEXT
320 GOSUB 150:REM PRINT HEADING
322 M=1: GOSUB 140:REM PRINT INPUT FUNCTION
324 PRINT:INPUT "C/R TO CONTINUE";A$
326 GOSUB 40:REM TAKE XFORM
328 GOSUB 220:REM PLOT DATA
330 PRINT "MORE (Y/N)?";
332 A$=INKEY$:IF A$="" THEN 332
334 IF A$="Y" OR A$="y" THEN 304
396 RETURN
1000 STOP
