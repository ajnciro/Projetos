import 'dart:io';

main(){
  //receber o peso da pessoa
  //receber a altura da pessoa
  //realizar cálculo
  //retornar IMC da pessoa
  var peso, altura;

  print("Digite seu peso: ");
  var inPeso = stdin.readLineSync();  peso = int.parse(inPeso);

  print("\nDigite sua altura: ");
  var inAlt = stdin.readLineSync();   altura = double.parse(inAlt);

  var imc = peso/(altura*altura);

  print("=================");
  print (imc);

}