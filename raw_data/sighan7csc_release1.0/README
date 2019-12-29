Bake-off 2013 CSC Datasets
Release 1.0
26 November 2013

This README file describes the data sets and evalaution procedure for the
SIGHAN-7 Bake-off: Chinese Spelling Check task.

The package is distributed freely with the following copyright
Copyright (C) 2013 Shih-Hung Wu, Chao-Lin Liu, Lung-Hao Lee
                   
Any questions regarding the datasets should be directed to
shwu@cyut.edu.tw, chaolin@nccu.edu.tw, lunghaolee@gmail.com


1. Directory Structure and Contents
===================================

The top-level directory has five subdirectories, namely

- ConfusionSet/  : The set of characters with similar shapes or pronunciations

- DryRun/  : The dryrun set used for output format validation
              
- EvaluationTool/  : The program used to evaluate the test data sets.  
              
- FinalTest/  : Each set contains 1000 Chinese texts selected from students’ essays which covered various common errors.
               Participants can employ any linguistic and computational resources to do identification and correction.

- SampleSet/  : The samples will be selected from students’ essays and released in XML format.
		Example:
		<DOC Nid="00018">
		<p>有些人會拿這次的教訓來勉勵自己，好讓自己在打混摸魚時警悌，使自己比以前更好、更進步。 </p>
	  <TEXT>
			<MISTAKE wrong_position=28>
				<wrong>警悌</wrong>
				<correct>警惕</correct>
			</MISTAKE>
    </TEXT>
    </DOC>
    
2. How to use the evaluation tool
================================================

java -jar sighan7csc.jar    
	-s : 1 for subtask-1 or 2 for subtask-2 (required)
  -i : file path of the system results (required)
  -t : file path of the ground truth (required)
  -o : file path of the detailed evaluation report (optional) 
  
(1) Evalaute results of subtask 1 with the detailed report
 
java -jar sighan7csc.jar -s 1 -i Toy_SubTask1_Result.txt -t Toy_SubTask1_Truth.txt -o Toy_SubTask1_Evalaution.txt

(2) Evalaute results of subtask 2 without the detailed report 

java -jar sighan7csc.jar -s 2 -i Toy_SubTask2_Result.txt -t Toy_SubTask2_Truth.txt    