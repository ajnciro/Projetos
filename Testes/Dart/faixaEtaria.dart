import 'dart:io';

main(){
	//var  imp = "Segunda Impressão...", te = " É a que fica";
  //print (imp);

 //var num1 = 13, num2 = 17;
 // print(num2 % num1);

 //print (imp + te);

/* var v1 = 10, v2 = 15;

 if (v1> v2){
   print (v1);]

 }else {
   print(v2);

 }*/

//var idade = stdin.readLineSync(); //texto
print("Digite uma idade:\n");
var input = stdin.readLineSync();
var idade = int.parse (input);

print(idade);

if (idade >=18 &&idade<50 ){
  print ("Maior de idade.");
}
else if (idade<18 && idade>12){
  print ("Adolescente.");
}
else if (idade > 50){
  print ("Idoso.");
}

}