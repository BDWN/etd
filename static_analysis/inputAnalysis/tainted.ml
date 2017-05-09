
open Cil
open Pretty

module E = Errormsg

(** compute use/def information *)

module VS = Set.Make (struct 
                        type t = Cil.varinfo
                        (* Subtraction is safe since vids are always positive*)
                        let compare v1 v2 = v1.vid - v2.vid
                      end)

let varUsed: VS.t ref = ref VS.empty
let varUsedFP: VS.t ref = ref VS.empty
  
  
let usedGlobalsVarsInFunc: (varinfo -> VS.t) ref  = ref (fun _ -> VS.empty)
let taintedParametersInFunc: (varinfo -> bool list) ref  = ref (fun _ -> [] )

let taintedReturnAnalysis = ref true

let selectLoopAndIf = ref false
let selectLoopOnly = ref false
let selectFloat = ref false
let selectPointer = ref false
let onlyDirect = ref false

class taintedVisitorClass : cilVisitor = object (self)
  inherit nopCilVisitor
      
  method vvrbl (v: varinfo) = 
    varUsed := VS.add v !varUsed;
    SkipChildren

  method vlval (l: lval) =
      match l with
	(Var vi, NoOffset) ->
          varUsed := VS.add vi !varUsed;
	  SkipChildren
      | (Var vi, Field(fi, NoOffset)) when not fi.fcomp.cstruct ->
          varUsed := VS.add vi !varUsed;
	  SkipChildren
      | _ -> DoChildren

  method vexpr (e:exp) =
    match e with
      Lval (Var v, off) -> 
        ignore (visitCilOffset (self :> cilVisitor) off);
          varUsed := VS.add v !varUsed;
        SkipChildren (* So that we do not see the v *)

    | AddrOf (Var v, off) 
    | StartOf (Var v, off) -> 
        ignore (visitCilOffset (self :> cilVisitor) off);
        varUsed := VS.add v !varUsed;
        SkipChildren

    | SizeOfE _
    | AlignOfE _ -> SkipChildren

    | _ -> DoChildren

  (* For function calls, do the transitive variable read/defs *)
  method vinst i = ignore(E.log "somethign wrong \n\n");
    match i with
    | Call (Some lvo, f, args, _) -> ignore (visitCilLval (self :> cilVisitor) lvo); List.iter (fun arg -> ignore (visitCilExpr (self :> cilVisitor) arg)) args; SkipChildren
    | Call (None, f, args, _) -> List.iter (fun arg -> ignore (visitCilExpr (self :> cilVisitor) arg)) args; SkipChildren
    | _ -> DoChildren
        
end  

let taintedVisitor = new taintedVisitorClass 





class taintedFPVisitorClass : cilVisitor = object (self)
  inherit nopCilVisitor

  method vvrbl (v: varinfo) = SkipChildren

  method vlval (l: lval) = DoChildren

  method vexpr (e:exp) =
(*     E.log "taintedFPVisitorClass Expr\n";  *)
    varUsed := VS.empty;

    match unrollType (Cil.typeOf e) with
        TFloat _ -> if (!selectFloat) then (
                    ignore (visitCilExpr taintedVisitor e); 
                    varUsedFP := VS.union !varUsedFP !varUsed;);
                    DoChildren
        | TPtr _ -> if (!selectPointer) then (ignore (visitCilExpr taintedVisitor e); 
                      varUsedFP := VS.union !varUsedFP !varUsed;);
                    DoChildren
        | _ ->   DoChildren

  (* For function calls, do the transitive variable read/defs *)
  method vinst i = DoChildren
        
end  

let taintedFPVisitor = new taintedFPVisitorClass 



(** Compute the use/def information for an instruction *)
let computeTaintedFPInstr (vs: VS.t) (i: instr) : VS.t = 
(*   E.log "TaintedAnalysis Instr\n"; *)
  varUsed := VS.empty;
  varUsedFP := VS.empty;
  let ve e = ignore (visitCilExpr taintedVisitor e)  in 
  let veFP e = ignore (visitCilExpr taintedFPVisitor e) in
  let rec doCallHelper pls bls = match (pls, bls) with
      e::pls' , true::bls' -> ignore (ve e); doCallHelper pls' bls'
    | e::pls' , false::bls' -> doCallHelper pls' bls'
    | [] , [] -> () 
    | e::pls' , [] -> ignore (ve e)
    | _ , _ -> ()
  in
    match i with 
    | Set ((Var(vi), _), e, _) -> ve e; veFP e; 
                        if (VS.mem vi vs)&& not !onlyDirect then 
                          VS.union !varUsedFP (VS.union vs !varUsed) 
                        else 
                          VS.union !varUsedFP vs
    | Call (Some (Var vi , _), Lval(Var viFN, _), args, _) ->  
                            ignore(doCallHelper args (!taintedParametersInFunc viFN));
                            if (VS.mem vi vs) then let 
                              usedVarsinFunc = !usedGlobalsVarsInFunc viFN
                            in 
                              VS.union !varUsed (VS.union vs usedVarsinFunc)
                            else 
                              VS.union !varUsed vs
    | Call (None, Lval(Var viFN, _), args, _) -> 
                            ignore(doCallHelper args (!taintedParametersInFunc viFN));
                            VS.union !varUsed vs
    | _ -> vs
    
    
let computeTaintedStmtKindFP (vs: VS.t) (sk: stmtkind) : VS.t =
  varUsed := VS.empty;
(*     E.log "TaintedAnalysis\n"; *)
  let ve e = ignore (visitCilExpr taintedFPVisitor e) in 
    match sk with 
    | ComputedGoto (e, _) 
    | If (e, _, _, _) 
    | Switch (e, _, _, _) 
    | Return (Some e, _) -> ve e; VS.union vs !varUsedFP
    | _ -> VS.union vs !varUsedFP
    

(** Compute the use/def information for an instruction *)
let computeTaintedInstr (vs: VS.t) (i: instr) : VS.t = 
  varUsed := VS.empty;
  let ve e = ignore (visitCilExpr taintedVisitor e) 
  in 
  let rec doCallHelper pls bls = match (pls, bls) with
      e::pls' , true::bls' -> ignore (ve e); doCallHelper pls' bls'
    | e::pls' , false::bls' -> doCallHelper pls' bls'
    | [] , [] -> () 
    | e::pls' , [] -> ignore (ve e)
    | _ , _ -> ()
  in
    match i with 
    | Set ((Var(vi), _), e, _) -> ve e; 
                        if (VS.mem vi vs) && not !onlyDirect then VS.union vs !varUsed else vs
    | Call (Some (Var vi , _), Lval(Var viFN, _), args, _) ->  
                            ignore(doCallHelper args (!taintedParametersInFunc viFN));
                            if (VS.mem vi vs) then let 
                              usedVarsinFunc = !usedGlobalsVarsInFunc viFN
                            in 
                              VS.union !varUsed (VS.union vs usedVarsinFunc)
                            else 
                              VS.union !varUsed vs
    | Call (None, Lval(Var viFN, _), args, _) -> 
                            ignore(doCallHelper args (!taintedParametersInFunc viFN));
                            VS.union !varUsed vs
    | _ -> vs
    

    
let breakInIfStmtKind (sk: stmtkind) (b: bool) = 
  match sk with 
     Break (_) -> b || true
    | _ -> b || false
    
    
let handleIfInLoopBlock b =
  List.fold_left (fun b s -> breakInIfStmtKind s.skind b; ) false b.bstmts

    
let ifInLoopStmtKind (sk: stmtkind) () =
  let ve e = ignore (visitCilExpr taintedVisitor e) in 
   let vs b = List.fold_left (fun b s -> breakInIfStmtKind s.skind b; ) false b.bstmts in 
    match sk with 
    | If (e, b1, b2, _) -> if (vs b1 || vs b2) then ve e else ()
    | Switch (e, b, _, _) -> if (vs b) then ve e else ();
    | _ -> ()

let handleLoopBlock b =
  List.fold_left (fun () s -> ifInLoopStmtKind s.skind (); ) ()
    b.bstmts


let computeTaintedStmtKindReturn (vs: VS.t) (sk: stmtkind) : VS.t =
  varUsed := VS.empty;
  let ve e = ignore (visitCilExpr taintedVisitor e) in 
    match sk with 
    | Return (Some e,l) -> ve e; VS.union vs !varUsed
    | _ -> vs

let computeTaintedStmtKindLoop (vs: VS.t) (sk: stmtkind) : VS.t =
  varUsed := VS.empty;
    match sk with 
    | ComputedGoto (e, _) 
    | If (e, _, _, _) 
    | Switch (e, _, _, _) -> vs;
    | Loop (b, _, _, _) -> handleLoopBlock b; VS.union vs !varUsed
    | _ -> vs

let computeTaintedStmtKindIf (vs: VS.t) (sk: stmtkind) : VS.t =
  varUsed := VS.empty;
  let ve e = ignore (visitCilExpr taintedVisitor e) in 
    match sk with 
    | ComputedGoto (e, _) 
    | If (e, _, _, _) 
    | Switch (e, _, _, _) -> ve e; VS.union vs !varUsed
    | _ -> vs

let computeTaintedStmtGeneralKind (vs: VS.t) (sk: stmtkind) : VS.t =
   if (!selectLoopOnly) then
        computeTaintedStmtKindLoop vs sk
   else if (!selectFloat || !selectPointer) then 
        computeTaintedStmtKindFP vs sk
   else
        computeTaintedStmtKindIf vs sk
    

let computeTaintedStmtKind (vs: VS.t) (sk: stmtkind) : VS.t =
   if (!taintedReturnAnalysis) 
        then computeTaintedStmtKindReturn vs sk
        else computeTaintedStmtGeneralKind vs sk

        

        
        
        
        
        
        

  
