IDENTIFICATION DIVISION.
PROGRAM-ID. LONG-PROGRAM.

DATA DIVISION.
WORKING-STORAGE SECTION.
01 COUNTER PIC 9(5).
01 MESSAGE PIC X(100) VALUE "This is a longer message to be displayed multiple times in the program. Hello, World!".

PROCEDURE DIVISION.
MAIN-PROCEDURE.
    PERFORM DISPLAY-MESSAGE VARYING COUNTER FROM 1 BY 1 UNTIL COUNTER > 3000.
    STOP RUN.

DISPLAY-MESSAGE.
    DISPLAY MESSAGE.
