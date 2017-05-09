Short notes about how to use the input analysis, which derives the set of variables which may influence a program's execution time.
The analysis is written as an extension of cil: https://github.com/cil-project/cil.


******Instalation****

1) Download cil:
git clone https://github.com/cil-project/cil.git

2) Copy files:
cp -r inputAnalysis [CILPATH]/src/ext/

3) Install cil using:
        ./configure 
        make
        make
        make install
        
******Usage******
Simply type
        cilly --doinputAnalysis  -c [INPUTFILE]
It will derive a list of input variables which may influence the execution time of a task, either due to branches (of any type) or loops. The results will be written to stdout.
        
cil is not able to handle pragma. Therefore first remove pragmas using the following sed command:
sed 's/_Pragma\((\s*\"[^"]*\"\s*)\)//' test.c  >test.c


