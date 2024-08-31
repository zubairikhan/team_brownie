# **Course project:** CV Reading
**Authors:** 
Milana Shkhanukova, Zubair Irfan Khan, Kevin Van Le, Katarina Baricova

**Course:** *Acquisition and analysis of eye-tracking data*

**Semester:** *Summer semester 2024*

## Project Description
Research Question: Does a picture in CVs influence the reader’s attention?

To fully address the primary research objective, our study aims to investigate the following key questions:

• Is there a reduction in time spent examining textual content when an
image is included?

• Which sections of resumes receive the most attention from viewers, and how does this differ between CVs with and without photographs?

Our main hypothesis is that participants will generally take longer to review
resumes that include a photograph of the applicant. Additionally, we anticipate
that the presence of a picture will serve as a distraction, leading to more errors
in participants’ evaluations or decisions regarding these resumes. 

## Instruction for a new student

For computing fixation durations for resume sections, run the notebook AnalysisV2.ipynb

Update the following file paths to point to the subject_files.txt and resume_names.txt in the data folder.

  subjects_to_include = "data/subject_files.txt"
  
  resumes_to_include = "data/resume_names.txt"
  
In the subject_files.txt, update the file paths to point to the .tsv files in data/subjects_tsv directory.




To create a randomized data for each participant run the sorting_algorithm.py script. There you need to specify the path to a folder where all of the resumes are saved. For each participant a separate cab will be created.




To plot the eye movement and/or bpogx/bpogy line Graph over time and/or heatmap, run the plot_eyemovement.py script



To compute the p value using the two sample t test and the effect size using Cohen's d for two sample groups, run the inferential_statistics.py script


## Overview of Folder Structure 

```
│projectdir          <- Project's main folder. It is initialized as a Git
│                       repository with a reasonable .gitignore file.
│
├── report           <- Report PDF
|
├── presentation     <- Final presentation slides (PDFs; optionally also .pptx etc)
|
├── _research        <- WIP scripts, code, notes, comments,
│                       to-dos and anything in a preliminary state.
│
├── plots            <- All exported plots go here, best in date folders.
|                       Note that to ensure reproducibility it is required that all plots can be
|                       recreated using the plotting scripts in the scripts folder.
│
├── scripts          <- Various scripts, e.g. analysis and plotting.
│                       The scripts use the `src` folder for their base code.
│
├── src              <- Source code for use in this project. Contains functions,
│                       structures and modules that are used throughout
│                       the project and in multiple scripts.
│
├── experiment       <- OpenSesame file to run the experiment; where applicable also stimuli, randomization
|
├── data             <- **If they have a reasonable file size**
|   ├── raw          <- Raw eye-tracking data
|   ├── preprocessed <- Data resulting from preprocessing
|
├── README.md        <- Top-level README. Fellow students need to be able to
|                       reproduce your project. Think about them!
|
├── .gitignore       <- List of files that you don’t want Git to automatically add
|                       (default Python .gitignore was used)
│
└── (requirements.txt)<- List of modules and packages that are used for your project
                     
```
## Note on sharing your recorded data
If your data is <1GB you can add it to the data folder in your Git repository. Otherwise, only include it in the project package that you submit on Ilias at the end of the term.
