async def prepare_case(order_id:str,summary:str,principal:dict)->dict:
 return {'order_id':order_id,'case_status':'DRAFT_ONLY','summary':summary[:200]}
