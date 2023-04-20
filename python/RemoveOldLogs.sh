#!/bin/bash


removeFiles(){

   name=$1
  
   output=${name//".log"/".out"}
   output=${output//"log"/"output"} 

   log=${name//".log"/".err"}
   log=${log//"log"/"error"}

   rm -rf  $name
   rm -rf  $output
   rm -rf  $log
 
   echo "....removing "$name
   echo "....removing "$output
   echo "....removing "$log 
 
}

prefix=$1

#echo $prefix

path="scripts/log/"$prefix"*"

array=($(ls $path))


if (( ${#array[@]} > 1  )); then
  
 echo " - More than one file"


  temp=""  

  for file in "${array[@]}"
  do

     #echo "$file"

     if [ -z "$temp" ]
     then

        temp=$file

        #echo "- temporal file : "$temp

     else

        if [ "$file" -ot "$temp" ]
        then
             echo "...File will be removed: "$file

             removeFiles $file

        else
             echo "...File will be removed: "$temp

             removeFiles $temp

             temp=$file

        fi


     fi

  

  done #loop over different files

fi 

