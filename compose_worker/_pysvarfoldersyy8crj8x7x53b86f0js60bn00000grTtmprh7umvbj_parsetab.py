
# _pysvarfoldersyy8crj8x7x53b86f0js60bn00000grTtmprh7umvbj_parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftTIMESDIVIDEleftPOWERrightUMINUSCOMMA COMPDEC DIVIDE EQUALS EVENTDEC FIXDEC FLUXBNDDEC FORCEFUNC FUNCDEC IN INITFUNC INT IRREV KEYWORD KEYWORDB LPAREN MINUS MULTICOMMENT NAME OBJFUNCDEC PLUS POOL POWER REACTION_ID REAL RPAREN RRULEDEC STOICH_COEF SYMBEQUI TIMEFUNC TIMES UNIT USERCNSTRDEC USERFUNCModel : Statement\n                 | Model Statement Statement : Fixed\n                     | FunctionDec\n                     | RateRuleDec\n                     | EventDec\n                     | ObjFuncDec\n                     | FluxBndDec\n                     | UserCnstrDec\n                     | CompartmentDec\n                     | ReactionLine\n                     | Initialise\n                     | Forcedfunc\n                     | Timefunc\n                     | Userfunc\n                     | Initfunc\n                     | NameInName\n                     | KeyWord\n                     | KeyWordB\n                     | Unit\n                     | MultiComment\n                     | SymbEquiNameInName : NAME IN NAMESymbEqui : SYMBEQUIMultiComment : MULTICOMMENTKeyWord : KEYWORDKeyWordB : KEYWORDBUnit : UNITFixed : FIXDEC FixListFunctionDec : FUNCDECRateRuleDec : RRULEDECEventDec : EVENTDECObjFuncDec : OBJFUNCDECFluxBndDec : FLUXBNDDECUserCnstrDec : USERCNSTRDECCompartmentDec : COMPDECForcedfunc : FORCEFUNCTimefunc : TIMEFUNCUserfunc : USERFUNCInitfunc : INITFUNCFixList : NAME\n                   | NAME FixListInitialise : NAME EQUALS ExpressionReactionLine : REACTION_ID ReactionEq\n                        | REACTION_ID ReactionEq ExpressionReactionEq : LeftHalfReaction EQUALS RightHalfReaction\n                      | LeftHalfReaction IRREV  RightHalfReaction\n                      | POOL EQUALS  RightHalfReaction\n                      | POOL IRREV  RightHalfReaction\n                      | LeftHalfReaction EQUALS POOL\n                      | LeftHalfReaction IRREV POOL LeftHalfReaction : SubstrateTerm\n                             | SubstrateTerm PLUS LeftHalfReaction RightHalfReaction : ProductTerm\n                              | ProductTerm PLUS RightHalfReactionSubstrateTerm : STOICH_COEF NAME\n                         | NAMEProductTerm : STOICH_COEF NAME\n                       | NAMEExpression : Expression PLUS Expression\n                      | Expression MINUS Expression\n                      | Expression TIMES Expression\n                      | Expression DIVIDE Expression\n                      | Power\n                      | Number\n                      | FuncPower : Expression POWER ExpressionExpression : MINUS Expression %prec UMINUSNumber : REAL\n                  | INT\n                  | NAMEFunc : LPAREN ArgList RPAREN\n                | NAME LPAREN ArgList RPARENArgList : Expression\n                   | ArgList COMMA Expression'
    
_lr_action_items = {'FIXDEC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[23,23,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'FUNCDEC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[24,24,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'RRULEDEC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[25,25,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'EVENTDEC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[26,26,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'OBJFUNCDEC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[27,27,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'FLUXBNDDEC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[28,28,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'USERCNSTRDEC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[29,29,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'COMPDEC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[30,30,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'REACTION_ID':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[31,31,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'NAME':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,39,40,41,42,43,44,45,49,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,70,71,72,73,74,75,76,77,80,81,82,83,84,85,86,87,88,90,91,92,93,94,96,97,98,99,100,102,],[32,32,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,44,-30,-31,-32,-33,-34,-35,-36,50,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,44,61,68,61,70,-42,-45,61,-64,-65,-66,-69,-70,-71,61,84,84,84,84,50,-43,-23,61,61,61,61,61,-68,61,-46,-50,-54,99,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,61,84,-58,-73,-55,]),'FORCEFUNC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[33,33,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'TIMEFUNC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[34,34,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'USERFUNC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[35,35,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'INITFUNC':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[36,36,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'KEYWORD':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[37,37,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'KEYWORDB':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[38,38,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'UNIT':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[39,39,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'MULTICOMMENT':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[40,40,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'SYMBEQUI':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[41,41,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,53,54,56,57,58,59,60,61,69,70,76,80,81,82,84,85,86,87,88,90,91,92,93,94,96,99,100,102,],[0,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-26,-27,-28,-25,-24,-2,-29,-41,-44,-42,-45,-64,-65,-66,-69,-70,-71,-43,-23,-68,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,-58,-73,-55,]),'POOL':([31,63,64,],[47,81,86,]),'STOICH_COEF':([31,63,64,65,66,67,98,],[49,83,83,83,83,49,83,]),'EQUALS':([32,46,47,48,50,68,89,],[51,63,65,-52,-57,-56,-53,]),'IN':([32,],[52,]),'MINUS':([45,51,54,55,56,57,58,59,60,61,62,69,71,72,73,74,75,76,77,79,80,81,82,84,85,86,87,88,90,91,92,93,94,96,97,99,100,101,102,],[55,55,72,55,-64,-65,-66,-69,-70,-71,55,72,55,55,55,55,55,-68,55,72,-46,-50,-54,-59,-47,-51,-48,-49,-60,-61,-62,-63,-67,-72,55,-58,-73,72,-55,]),'REAL':([45,51,55,62,71,72,73,74,75,77,80,81,82,84,85,86,87,88,97,99,102,],[59,59,59,59,59,59,59,59,59,59,-46,-50,-54,-59,-47,-51,-48,-49,59,-58,-55,]),'INT':([45,51,55,62,71,72,73,74,75,77,80,81,82,84,85,86,87,88,97,99,102,],[60,60,60,60,60,60,60,60,60,60,-46,-50,-54,-59,-47,-51,-48,-49,60,-58,-55,]),'LPAREN':([45,51,55,61,62,71,72,73,74,75,77,80,81,82,84,85,86,87,88,97,99,102,],[62,62,62,77,62,62,62,62,62,62,62,-46,-50,-54,-59,-47,-51,-48,-49,62,-58,-55,]),'IRREV':([46,47,48,50,68,89,],[64,66,-52,-57,-56,-53,]),'PLUS':([48,50,54,56,57,58,59,60,61,68,69,76,79,82,84,90,91,92,93,94,96,99,100,101,],[67,-57,71,-64,-65,-66,-69,-70,-71,-56,71,-68,71,98,-59,-60,-61,-62,-63,-67,-72,-58,-73,71,]),'TIMES':([54,56,57,58,59,60,61,69,76,79,90,91,92,93,94,96,100,101,],[73,-64,-65,-66,-69,-70,-71,73,-68,73,73,73,-62,-63,-67,-72,-73,73,]),'DIVIDE':([54,56,57,58,59,60,61,69,76,79,90,91,92,93,94,96,100,101,],[74,-64,-65,-66,-69,-70,-71,74,-68,74,74,74,-62,-63,-67,-72,-73,74,]),'POWER':([54,56,57,58,59,60,61,69,76,79,90,91,92,93,94,96,100,101,],[75,-64,-65,-66,-69,-70,-71,75,-68,75,75,75,75,75,-67,-72,-73,75,]),'RPAREN':([56,57,58,59,60,61,76,78,79,90,91,92,93,94,95,96,100,101,],[-64,-65,-66,-69,-70,-71,-68,96,-74,-60,-61,-62,-63,-67,100,-72,-73,-75,]),'COMMA':([56,57,58,59,60,61,76,78,79,90,91,92,93,94,95,96,100,101,],[-64,-65,-66,-69,-70,-71,-68,97,-74,-60,-61,-62,-63,-67,97,-72,-73,-75,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Model':([0,],[1,]),'Statement':([0,1,],[2,42,]),'Fixed':([0,1,],[3,3,]),'FunctionDec':([0,1,],[4,4,]),'RateRuleDec':([0,1,],[5,5,]),'EventDec':([0,1,],[6,6,]),'ObjFuncDec':([0,1,],[7,7,]),'FluxBndDec':([0,1,],[8,8,]),'UserCnstrDec':([0,1,],[9,9,]),'CompartmentDec':([0,1,],[10,10,]),'ReactionLine':([0,1,],[11,11,]),'Initialise':([0,1,],[12,12,]),'Forcedfunc':([0,1,],[13,13,]),'Timefunc':([0,1,],[14,14,]),'Userfunc':([0,1,],[15,15,]),'Initfunc':([0,1,],[16,16,]),'NameInName':([0,1,],[17,17,]),'KeyWord':([0,1,],[18,18,]),'KeyWordB':([0,1,],[19,19,]),'Unit':([0,1,],[20,20,]),'MultiComment':([0,1,],[21,21,]),'SymbEqui':([0,1,],[22,22,]),'FixList':([23,44,],[43,53,]),'ReactionEq':([31,],[45,]),'LeftHalfReaction':([31,67,],[46,89,]),'SubstrateTerm':([31,67,],[48,48,]),'Expression':([45,51,55,62,71,72,73,74,75,77,97,],[54,69,76,79,90,91,92,93,94,79,101,]),'Power':([45,51,55,62,71,72,73,74,75,77,97,],[56,56,56,56,56,56,56,56,56,56,56,]),'Number':([45,51,55,62,71,72,73,74,75,77,97,],[57,57,57,57,57,57,57,57,57,57,57,]),'Func':([45,51,55,62,71,72,73,74,75,77,97,],[58,58,58,58,58,58,58,58,58,58,58,]),'ArgList':([62,77,],[78,95,]),'RightHalfReaction':([63,64,65,66,98,],[80,85,87,88,102,]),'ProductTerm':([63,64,65,66,98,],[82,82,82,82,82,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Model","S'",1,None,None,None),
  ('Model -> Statement','Model',1,'p_model','PyscesParse.py',680),
  ('Model -> Model Statement','Model',2,'p_model','PyscesParse.py',681),
  ('Statement -> Fixed','Statement',1,'p_statement','PyscesParse.py',686),
  ('Statement -> FunctionDec','Statement',1,'p_statement','PyscesParse.py',687),
  ('Statement -> RateRuleDec','Statement',1,'p_statement','PyscesParse.py',688),
  ('Statement -> EventDec','Statement',1,'p_statement','PyscesParse.py',689),
  ('Statement -> ObjFuncDec','Statement',1,'p_statement','PyscesParse.py',690),
  ('Statement -> FluxBndDec','Statement',1,'p_statement','PyscesParse.py',691),
  ('Statement -> UserCnstrDec','Statement',1,'p_statement','PyscesParse.py',692),
  ('Statement -> CompartmentDec','Statement',1,'p_statement','PyscesParse.py',693),
  ('Statement -> ReactionLine','Statement',1,'p_statement','PyscesParse.py',694),
  ('Statement -> Initialise','Statement',1,'p_statement','PyscesParse.py',695),
  ('Statement -> Forcedfunc','Statement',1,'p_statement','PyscesParse.py',696),
  ('Statement -> Timefunc','Statement',1,'p_statement','PyscesParse.py',697),
  ('Statement -> Userfunc','Statement',1,'p_statement','PyscesParse.py',698),
  ('Statement -> Initfunc','Statement',1,'p_statement','PyscesParse.py',699),
  ('Statement -> NameInName','Statement',1,'p_statement','PyscesParse.py',700),
  ('Statement -> KeyWord','Statement',1,'p_statement','PyscesParse.py',701),
  ('Statement -> KeyWordB','Statement',1,'p_statement','PyscesParse.py',702),
  ('Statement -> Unit','Statement',1,'p_statement','PyscesParse.py',703),
  ('Statement -> MultiComment','Statement',1,'p_statement','PyscesParse.py',704),
  ('Statement -> SymbEqui','Statement',1,'p_statement','PyscesParse.py',705),
  ('NameInName -> NAME IN NAME','NameInName',3,'p_nameinname','PyscesParse.py',709),
  ('SymbEqui -> SYMBEQUI','SymbEqui',1,'p_inequalities_symb','PyscesParse.py',713),
  ('MultiComment -> MULTICOMMENT','MultiComment',1,'p_multicomment','PyscesParse.py',718),
  ('KeyWord -> KEYWORD','KeyWord',1,'p_keyword','PyscesParse.py',722),
  ('KeyWordB -> KEYWORDB','KeyWordB',1,'p_keywordboolean','PyscesParse.py',731),
  ('Unit -> UNIT','Unit',1,'p_unit','PyscesParse.py',743),
  ('Fixed -> FIXDEC FixList','Fixed',2,'p_fixed','PyscesParse.py',763),
  ('FunctionDec -> FUNCDEC','FunctionDec',1,'p_functiondec','PyscesParse.py',767),
  ('RateRuleDec -> RRULEDEC','RateRuleDec',1,'p_rateruledec','PyscesParse.py',778),
  ('EventDec -> EVENTDEC','EventDec',1,'p_eventdec','PyscesParse.py',789),
  ('ObjFuncDec -> OBJFUNCDEC','ObjFuncDec',1,'p_objfuncdec','PyscesParse.py',854),
  ('FluxBndDec -> FLUXBNDDEC','FluxBndDec',1,'p_fluxbnddec','PyscesParse.py',883),
  ('UserCnstrDec -> USERCNSTRDEC','UserCnstrDec',1,'p_usercnstrdec','PyscesParse.py',912),
  ('CompartmentDec -> COMPDEC','CompartmentDec',1,'p_compartmentdec','PyscesParse.py',959),
  ('Forcedfunc -> FORCEFUNC','Forcedfunc',1,'p_forcedfunc','PyscesParse.py',985),
  ('Timefunc -> TIMEFUNC','Timefunc',1,'p_timefunc','PyscesParse.py',996),
  ('Userfunc -> USERFUNC','Userfunc',1,'p_userfunc','PyscesParse.py',1001),
  ('Initfunc -> INITFUNC','Initfunc',1,'p_initfunc','PyscesParse.py',1012),
  ('FixList -> NAME','FixList',1,'p_fixedreagents','PyscesParse.py',1021),
  ('FixList -> NAME FixList','FixList',2,'p_fixedreagents','PyscesParse.py',1022),
  ('Initialise -> NAME EQUALS Expression','Initialise',3,'p_initialise','PyscesParse.py',1034),
  ('ReactionLine -> REACTION_ID ReactionEq','ReactionLine',2,'p_reaction_line','PyscesParse.py',1054),
  ('ReactionLine -> REACTION_ID ReactionEq Expression','ReactionLine',3,'p_reaction_line','PyscesParse.py',1055),
  ('ReactionEq -> LeftHalfReaction EQUALS RightHalfReaction','ReactionEq',3,'p_reaction_eq','PyscesParse.py',1110),
  ('ReactionEq -> LeftHalfReaction IRREV RightHalfReaction','ReactionEq',3,'p_reaction_eq','PyscesParse.py',1111),
  ('ReactionEq -> POOL EQUALS RightHalfReaction','ReactionEq',3,'p_reaction_eq','PyscesParse.py',1112),
  ('ReactionEq -> POOL IRREV RightHalfReaction','ReactionEq',3,'p_reaction_eq','PyscesParse.py',1113),
  ('ReactionEq -> LeftHalfReaction EQUALS POOL','ReactionEq',3,'p_reaction_eq','PyscesParse.py',1114),
  ('ReactionEq -> LeftHalfReaction IRREV POOL','ReactionEq',3,'p_reaction_eq','PyscesParse.py',1115),
  ('LeftHalfReaction -> SubstrateTerm','LeftHalfReaction',1,'p_left_half_reaction','PyscesParse.py',1136),
  ('LeftHalfReaction -> SubstrateTerm PLUS LeftHalfReaction','LeftHalfReaction',3,'p_left_half_reaction','PyscesParse.py',1137),
  ('RightHalfReaction -> ProductTerm','RightHalfReaction',1,'p_right_half_reaction','PyscesParse.py',1147),
  ('RightHalfReaction -> ProductTerm PLUS RightHalfReaction','RightHalfReaction',3,'p_right_half_reaction','PyscesParse.py',1148),
  ('SubstrateTerm -> STOICH_COEF NAME','SubstrateTerm',2,'p_substrate_term','PyscesParse.py',1159),
  ('SubstrateTerm -> NAME','SubstrateTerm',1,'p_substrate_term','PyscesParse.py',1160),
  ('ProductTerm -> STOICH_COEF NAME','ProductTerm',2,'p_product_term','PyscesParse.py',1175),
  ('ProductTerm -> NAME','ProductTerm',1,'p_product_term','PyscesParse.py',1176),
  ('Expression -> Expression PLUS Expression','Expression',3,'p_rate_eq','PyscesParse.py',1190),
  ('Expression -> Expression MINUS Expression','Expression',3,'p_rate_eq','PyscesParse.py',1191),
  ('Expression -> Expression TIMES Expression','Expression',3,'p_rate_eq','PyscesParse.py',1192),
  ('Expression -> Expression DIVIDE Expression','Expression',3,'p_rate_eq','PyscesParse.py',1193),
  ('Expression -> Power','Expression',1,'p_rate_eq','PyscesParse.py',1194),
  ('Expression -> Number','Expression',1,'p_rate_eq','PyscesParse.py',1195),
  ('Expression -> Func','Expression',1,'p_rate_eq','PyscesParse.py',1196),
  ('Power -> Expression POWER Expression','Power',3,'p_power','PyscesParse.py',1206),
  ('Expression -> MINUS Expression','Expression',2,'p_uminus','PyscesParse.py',1212),
  ('Number -> REAL','Number',1,'p_number','PyscesParse.py',1218),
  ('Number -> INT','Number',1,'p_number','PyscesParse.py',1219),
  ('Number -> NAME','Number',1,'p_number','PyscesParse.py',1220),
  ('Func -> LPAREN ArgList RPAREN','Func',3,'p_function','PyscesParse.py',1259),
  ('Func -> NAME LPAREN ArgList RPAREN','Func',4,'p_function','PyscesParse.py',1260),
  ('ArgList -> Expression','ArgList',1,'p_arglist','PyscesParse.py',1297),
  ('ArgList -> ArgList COMMA Expression','ArgList',3,'p_arglist','PyscesParse.py',1298),
]
