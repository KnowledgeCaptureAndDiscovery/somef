# easytv-annotator
Sign language annotator library for the EASYTV european project


TRANSLATOR PROJECT

## Prerequisites
Project is linked to the easytv project resources: https://github.com/oeg-upm/easytv-resources

It uses Perl for TreeTagger. Install utf8
> perl -MCPAN -e shell
> install utf8::all


## Installation

This project is compiled with maven and there are four libraries that are not available at maven central repo.
These jar are in the /lib folder and must be added to your local maven repo. 

### Easy way

Using maven through the command install. The pom file contains all the instructions to install the dependencies

```sh
$ mvn install
```

### Hard way
Through commands: The basic comand is 
```sh
$ mvn install:install-file -Dfile=${jarfile} -DgroupId=${group.id} -DartifactId=${lib.id} -Dversion=${version} -Dpackaging=jar
```

Example: 
```sh
$ cd lib
$ mvn install:install-file -Dfile=lib/babelnet-api-3.7.1.jar -DgroupId=it.uniroma1.lcl.babelnet -DartifactId=babelnet-api -Dversion=3.7.1 -Dpackaging=jar
```

There is a .bat file and a .sh file for install all the dependencies: 
- InstallDependencies.sh
- InstallDependencies.bat




## Build

First build the project with maven.
The compiled jar of the project is copied to the /dist folder, with all the necessary libraries.

## Execution
To execute the project you can work on your own IDE and run the class 'Execution' or execute the compiled jar as

```sh
$ cd dist
$ java -jar EasyTranslator-1.0.jar
```

The execution provides a console in which you can write sentences specifiying their language. The program parses the sentence with CoreNLP and asks BabelNet synsets for Verbs and Nouns. Then, the program sends the sentence to BabelFly


## Properties

BabelNet and BabelFly need two specific folders in the root folder: config and resources.
These two are repeated in the project root folder and in the dist folder. 


Personal keys for accessing BabelNet and BabelFly are introduced in the files:
- config/babelfy.var.properties
- config/babelnet.var.properties



