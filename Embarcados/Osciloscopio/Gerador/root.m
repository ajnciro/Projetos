(* ::Package:: *)

(* ::Input:: *)
(*arduino=DeviceOpen["Arduino","COM3"];*)
(*write[vol_]:=DeviceWrite[arduino,6->Quantity[vol,"Volts"]];*)
(**)
(*SawtoothWave[{0,5},\[Omega] n];*)
(*TriangleWave[{0,5},\[Omega] n];*)
(*SquareWave[{0,5},\[Omega] n];*)
(*SinWave[\[Omega]_,r_]:=If[r==0,(5*Sin[\[Omega] Pi n]+5)/2,((Sin[\[Omega] Pi n]+Sin[(RandomReal[r*{\[Omega],3\[Omega]}])*Pi n])+2)*5/4];*)
