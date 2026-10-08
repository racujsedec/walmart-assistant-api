def reciprocal_rank_fusion(ranked_lists:list[list[str]],k:int=60)->list[str]:
 scores={}
 for ids in ranked_lists:
  for rank,id_ in enumerate(ids,1):scores[id_]=scores.get(id_,0)+1/(k+rank)
 return sorted(scores,key=scores.get,reverse=True)
