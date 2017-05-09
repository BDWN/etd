open Cil
open Feature
open Pretty

module DF = Dataflow
module UD = Tainted
module IH = Inthash
module E = Errormsg
module VS = UD.VS

let debug = ref false
let verbose = ref false

let selectLoopOnly = ref false
let selectLoopAndIf = ref false
let selectFloat = ref false
let selectPointer = ref false

let onlyDirect = ref false

let debug_print () vs = (VS.fold
    (fun vi d -> 
      d ++ text "Var: " ++ text vi.vname
	++ text " id: " ++ num vi.vid ++ text " ")
    vs nil) ++ line

let printer = ref debug_print

let usedGlobalsVarsInFuncTuple = ref debug_print 

let interProcedural = ref  true


                                
let usedGlobalsVarsInFuncList: (varinfo * VS.t) list ref  = ref []

let rec updateUsedGlobalsVarsInFuncListHelper inLS (vi:varinfo) (vs: VS.t) outLS  = match inLS with
                                (v,x)::ls ->  if (String.compare vi.vname v.vname = 0) then (List.append ((vi,vs)::outLS) ls) 
                                                else (updateUsedGlobalsVarsInFuncListHelper ls vi vs) ((v,x)::outLS)
                                |[] ->         ((vi,vs)::outLS)

let updateUsedGlobalsVarsInFuncList (vi:varinfo) (vs: VS.t) = 
                let newLS = updateUsedGlobalsVarsInFuncListHelper !usedGlobalsVarsInFuncList vi vs []
                in usedGlobalsVarsInFuncList := newLS

let rec findInUsedGlobalsVarsInFuncList inLS (vi:varinfo) = match inLS with
                                 (v,vs)::ls -> if (vi.vname = v.vname) then (vs) else (findInUsedGlobalsVarsInFuncList ls vi)
                                |[] -> VS.empty
                  
                  
let usedGlobalsVarsInFunc: (varinfo -> VS.t) ref  = ref (fun vi -> findInUsedGlobalsVarsInFuncList !usedGlobalsVarsInFuncList vi)





let taintedParametersInFuncList: (varinfo * bool list) list ref  = ref []

let rec updateTaintedParametersInFuncListHelper inLS (vi:varinfo) (bl: bool list) outLS  = 
                                match inLS with
                                 (v,bl2)::ls -> if (String.compare vi.vname v.vname = 0) then (List.append ((vi,bl)::outLS) ls)
                                              else (updateTaintedParametersInFuncListHelper ls vi bl ((v,bl2)::outLS))
                                |[] ->        ((vi,bl)::outLS)

let rec findInTaintedParametersInFuncList inLS (vi:varinfo) = match inLS with
                                 (v,bl)::ls ->  if (vi.vname = v.vname) then (bl) else (findInTaintedParametersInFuncList ls vi)
                                |[] -> []

let taintedParametersInFunc: (varinfo -> bool list) ref  = ref (fun vi -> findInTaintedParametersInFuncList !taintedParametersInFuncList vi)

                                
let updateTaintedParametersInFuncList (vi:varinfo) (bl: bool list) = 
(*                ignore(E.log "updateTaintedParametersInFuncList1 %s Size of paramList: %i \n" vi.vname (List.length !taintedParametersInFuncList)); *)
                let newLS = updateTaintedParametersInFuncListHelper !taintedParametersInFuncList vi bl []
                in 
(*                  ignore(E.log "updateTaintedParametersInFuncList2 %s Size of paramList: %i \n" vi.vname (List.length !taintedParametersInFuncList)); *)
                  taintedParametersInFuncList := newLS;
(*                  ignore(E.log "updateTaintedParametersInFuncList3 %s Size of paramList: %i \n" vi.vname (List.length !taintedParametersInFuncList)); *)
                  taintedParametersInFunc := (fun vi ->  findInTaintedParametersInFuncList newLS vi)
                  





(* Data Flow Analysis *)
module IAFlow = struct
  (* For debugging purposes *)
  let name = "inputAnalysis"
  
  (* Whether to turn on debugging *)
  let debug = debug

  (* The type of the data we compute for each block start *)
  type t = VS.t

  (* Pretty-print the state *)
  let pretty () vs =
    let fn = !printer in
    fn () vs
    
  (* For each block id, the data at the start. *)  
  let stmtStartData = IH.create 32

  (* The data at function exit. Used for statements with no successors. This is usually bottom, since we'll also use doStmt on Return statements.*)
  let funcExitData = VS.empty

  (* When the analysis reaches the start of a block *)
  let combineStmtStartData (stm:stmt) ~(old:t) (now:t) =
    if not(VS.compare old now = 0)
    then Some(VS.union old now)
    else None

  (* Take the data from two successors and combine it *)
  let combineSuccessors = VS.union

  (* The (backwards) transfer function for a branch. *)
  let doStmt stmt =
(*    ignore(E.log "looking at: %a\n" d_stmt stmt);*)
    let handle_stm vs = match stmt.skind with
      Instr _ -> vs
    | s -> UD.computeTaintedStmtKind vs s
    in
    DF.Post handle_stm

  (* The (backwards) transfer function for an instruction. *)
  let doInstr i vs =
    let transform vs' = UD.computeTaintedInstr vs i 
    in
    DF.Post transform

  (* Whether to put this predecessor block in the worklist *)
  let filterStmt stm1 stm2 = true

end
module L = DF.BackwardsDataFlow(IAFlow)



(* add all statements to hash and to all_stmt *)
let all_stmts = ref []

class nullAdderClass = object(self)
  inherit nopCilVisitor

  method vstmt s =
(*     E.log "vstmt %a\n" d_stmt s; *)
    all_stmts := s :: (!all_stmts);
    IH.add IAFlow.stmtStartData s.sid VS.empty;
    DoChildren
end

let null_adder fdec =
(*   E.log "\n null_adder Add Statement of Function %s \n" fdec.svar.vname; *)
  ignore(visitCilFunction (new nullAdderClass) fdec);
  !all_stmts


(* to run the data flow analysis *)
let computeInputAnalysis fdec =
  IH.clear IAFlow.stmtStartData;
  all_stmts := [];
  let a = null_adder fdec in
  try
(*     E.log "try L.compute \n"; *)
    L.compute a
  with E.Error -> begin
    ignore(E.log "InputAnalysis failed on function:\n %a\n" d_global (GFun(fdec,locUnknown)));
    E.s "Bug in InputAnalysis compute"
  end

  
(* Print Output: tainted variables *)
let resultSet = ref VS.empty
  
let collectLocal vs initSet = VS.fold (fun vi set -> VS.add vi set) vs initSet
  
let collect set = IH.fold (fun i vs initSet -> collectLocal vs initSet)  IAFlow.stmtStartData set

let printSetTemp set str = 
  let d = VS.fold (fun vi d -> d ++ text vi.vname ++ text " ") in 
        ignore(printf "All variables used for return in %s: %t" str (fun () -> (d set nil) ++ line))

let printSet set = 
  let d = VS.fold (fun vi d -> d ++ text vi.vname ++ text " ") in 
        if (!verbose) then 
           ( ignore(printf "All input-influencing variables: %t" (fun () -> (d set nil) ++ line)); 
           ignore(printf "Global input-influencing variables: %t" (fun () -> (d (VS.filter (fun vi -> vi.vglob) set)  nil) ++ line)))
           else if (not !verbose) then ignore(printf "%t" (fun () -> (d (VS.filter (fun vi -> vi.vglob) set)  nil) ++ line))
  


(*  to collect all variables within a function and add it to usedGlobalsVarsInFunc *)
let computeUsedGlobalsVarsInFunc fdec = 
  if !interProcedural then ( updateUsedGlobalsVarsInFuncList fdec.svar (collect VS.empty)
 (* let usedGlobalsVarsInFunc' = !usedGlobalsVarsInFunc in
    let varUsed = collect VS.empty  in 
      usedGlobalsVarsInFunc := (fun name ->  if name = fdec.svar then varUsed else usedGlobalsVarsInFunc' name )
 *) )
  else ()
  
(*  to fill the list of tainted params with initial value false *)
let fillParamList fdec = 
  if !interProcedural then (
    let paraList = List.fold_left (fun res fdecL -> match fdecL with  _ -> false::res ) [] fdec.sformals in      
     updateTaintedParametersInFuncList fdec.svar  paraList   
  )
  else ()


class doPreComputation = object(self)
  inherit nopCilVisitor

  method vfunc fd = Cfg.clearCFGinfo fd;
        ignore(Cfg.cfgFun fd);
        
        UD.varUsed := VS.empty; 
        UD.taintedReturnAnalysis := true;
(*         ignore(E.log "Fill  %s \n" fd.svar.vname);   *)
(*         List.iter (fun decl-> ignore(E.log "Fill  %i \n" decl.vid)) fd.sformals; *)
        computeInputAnalysis fd;
        computeUsedGlobalsVarsInFunc fd;
(*         ignore(E.log "Fill  %s \n" fd.svar.vname);   *)
(*         List.iter (fun decl-> ignore(E.log "Fill  %i \n" decl.vid)) fd.sformals; *)
(*         ignore(E.log "fillParamList1 %s \n" fd.svar.vname);   *)
        !usedGlobalsVarsInFunc fd.svar;
(*         printSetTemp (!usedGlobalsVarsInFunc fd.svar) fd.svar.vname;         *)
        fillParamList fd;
        DoChildren;
end




let finished = ref false       

(*  to fill the list of tainted params with initial value false *)
let rec selectTaintedParamList pl ls nls tSet = 
(*   ignore(E.log ("    selectTaintedParamList: ")); *)
  if !interProcedural then (
  match (pl, ls)  with 
      p::pll, true::lls -> if VS.mem p tSet 
                            then selectTaintedParamList pll lls (true::nls) tSet
                            else (ignore(E.log ("Error: value set from true to false.\n"));selectTaintedParamList pll lls (false::nls) tSet)
    | p::pll, false::lls -> if VS.mem p tSet 
                             then (finished := false; selectTaintedParamList pll lls (true::nls) tSet)
                             else selectTaintedParamList pll lls (false::nls) tSet
    | [], [] ->  nls
    | _, _ -> ignore(E.log ("Error: Unequal list sizes. \n")); []
  ) else []
    
(*  to update the list of tainted params with initial value false *)
let updateTaintedParamList fdec nls = 
  if !interProcedural then (updateTaintedParametersInFuncList fdec.svar nls
(*   let taintedParametersInFunc' = !taintedParametersInFunc in *)
(*       taintedParametersInFunc := (fun name ->  if name = fdec.svar then (  (*ignore(E.log "Then statement %s \n" name.vname);*) nls) else (   *)
(*       (*ignore(E.log "Else statement %s \n" name.vname);*) taintedParametersInFunc' name)) *)
  )
  else ()


class doFeatureClass = object(self)
  inherit nopCilVisitor

  method vfunc fd = Cfg.clearCFGinfo fd;
(*         ignore(Cfg.cfgFun fd); *)
        UD.varUsed := VS.empty; 
        UD.taintedReturnAnalysis := false;
(*         ignore(E.log "doFeatureClass pre: %s \n." fd.svar.vname); *)
        computeInputAnalysis fd;
        let resultSet' = collect VS.empty in 
          resultSet := VS.union resultSet' !resultSet;
(*        ignore(E.log "doFeatureClass after: %s size = %i\n." fd.svar.vname  (List.length fd.sformals)); *)
       
       
        let ls = !taintedParametersInFunc fd.svar in   
(*            ignore(E.log "doFeatureClass after: %s size = %i Res: %i\n." fd.svar.vname  (List.length fd.sformals) (List.length ls)); *)
           let nls = List.rev(selectTaintedParamList  fd.sformals ls [] resultSet') in 
                updateTaintedParamList fd nls;
(*         ignore(E.log "doFeatureClass done: %s \n\n." fd.svar.vname); *)
        
        DoChildren;
end

let rec do_input_analysis_second (i : int) (f:file) = 
(*         ignore(E.log "Do Second Analysis\n"); *)
        if (!finished || i = 0) then () else
        (
(*           ignore(E.log "iteration i = %i \n" i); *)
          finished := true;
          visitCilFile (new doFeatureClass) f; 
(*           ignore(E.log "after visit class \n"); *)
          UD.taintedParametersInFunc := !taintedParametersInFunc;
          do_input_analysis_second (i-1) f;
        )

let do_input_analysis_complete (f:file) = 
(*   ignore(E.log "CompleteAnalysis\n"); *)
  UD.selectLoopAndIf := !selectLoopAndIf;
  UD.selectLoopOnly := !selectLoopOnly;
  UD.selectFloat := !selectFloat;
  UD.selectPointer := !selectPointer;
  UD.onlyDirect := !onlyDirect;
(*   ignore(E.log "all input stuff set\n"); *)
  
  visitCilFile (new doPreComputation) f; 
(*   ignore(E.log "visiter Done\n"); *)
  UD.usedGlobalsVarsInFunc := !usedGlobalsVarsInFunc;
  UD.taintedParametersInFunc := !taintedParametersInFunc;

(*   ignore(E.log "CompleteAnalysis 2 Step\n"); *)
  do_input_analysis_second 10 f;  
  
  printSet !resultSet


let feature =
  {
   fd_name = "inputAnalysis";
   fd_enabled = false;
   fd_description = "Derive which variables influence the timing";
   fd_extraopt = [   
   "--ia_verbose", Arg.Unit (fun n -> verbose := true)," Print lots of debugging info";
   "--ia_direct", Arg.Unit (fun n -> onlyDirect := true)," Only print variable directly influencing the exec time.";
   "--ia_loopOnly", Arg.Unit (fun n -> selectLoopOnly := true)," Compute only loop variables";
   "--ia_float", Arg.Unit (fun n -> selectFloat := true)," Print lots of debugging info";
   "--ia_pointer", Arg.Unit (fun n -> selectPointer := true)," Print lots of debugging info";
   "--ia_noIP", Arg.Unit (fun n -> interProcedural := false)," Do not perform an interprocedural analysis";
   "--ia_all", Arg.Unit (fun n -> selectLoopAndIf := true; 
                                selectPointer := false; 
                                selectFloat := false; 
                                selectLoopOnly := false)," Compute all variables";
   ];
   fd_doit = do_input_analysis_complete;
   fd_post_check = false
 }

let () = Feature.register feature
