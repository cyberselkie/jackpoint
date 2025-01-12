import dice

class roll():
    """
    Description:
    Roll the dice, babygirl.
    """
    def __init__(self, rating) -> None:
        self.rating = rating

    def dice_base(self, rating, edge):
        if edge is not None:
            edge_roll = dice.roll(f'{rating}d6x')
            final_rolls = edge_roll
        else:
            dice_roll = dice.roll(f'{rating}d6')
            final_rolls = dice_roll
        return(final_rolls)

    def hits(self, rating, edge):
        result = self.dice_base(rating, edge)
        print(result)
        hits = 0
        ones = 0
        for n in result:
            print(n)
            if n >= 5:
                hits += 1
            elif n == 1:
                ones += 1
            else: pass
            if ones >= len(result)/2:
                err = True #glitch or crit glitch!
                break
            else:
                err = False
        response = [hits, ones, err, result]
        print(response)
        return response #HITS 0 ONES 1 ERR 2 RESULT 3

    def extended_test(self, rating, edge, tn):
        ex_test_list = []
        ex_test = 0
        timer = 0
        rolls_list = []
        error = None

        rolls_dict = {} #final form of info for the return value: dict
        while ex_test < tn:
            result = self.hits(rating, edge) #0 HITS ONES 1 ERR 2 ROLL 3
            print(result)
            ex_test_list.append(result[0])
            ex_test += result[0]  #count the hits
            print(ex_test)
            timer += 1
            rolls_list.append(result[3]) #add what was actually rolled
            if result[2] is True: #check if err is True
                error = True
                break
            else: pass
        rolls_dict["hits"] = ex_test
        rolls_dict["hits_list"] = ex_test_list
        rolls_dict["timer"] = timer
        rolls_dict["rolls"] = rolls_list
        rolls_dict["error"] = error

        return rolls_dict

    #def skill_roll(self, rating):
        