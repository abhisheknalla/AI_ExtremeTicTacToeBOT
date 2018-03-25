import random
import sys
import copy
import time

######################################GIVE HIGHER PRIORITY TO NON CORNER POINTS FOR DIAMONS#############################

class Team31():
    def __init__(self):
        self.MaxDepth = 3

        self.win_move = False

        self.win_player = None

        self.Util_Matrix = [
                            [0    ,-1 ,-10 ,-100,-1000],
                            [1    ,1  , 10 , 100,    0],
                            [10   ,0  ,  0 ,   0,    0],
                            [100  ,0  ,  0 ,   0,    0],
                            [1000 ,0  ,  0 ,   0,    0]
                             ]###SERIOUSLY CHECK THESE VALUES

        self.cellWts =[[2,3,3,2],[3,4,4,3],[3,4,4,3],[2,3,3,2]]
        self.blockWts = [[6,4,4,6],[4,3,3,4],[4,3,3,4],[6,4,4,6]]

        self.win_once_flag = False

        self.horizontal = []

        self.vertical = []

        for i in range(4):
            new = []
            for j in  range(4):
                new.append([i,j])
            self.horizontal.append(new)

        for j in range(4):
            new = []
            for i in range(4):
                new.append([i,j])
            self.vertical.append(new)

        self.cntp = 0 # how many blocks won by player
        self.cnto = 0 # how many blocks won by opponent
        pass

    def MinMax(self, board, old_move, node_type_maxnode, player_sign, depth, alpha, beta, best_row, best_coloumn, itr_max_depth,st_time):

        if (time.time() - st_time)>15.7:
            utility = 0
            return (utility, best_row, best_coloumn)

        if player_sign == 'x':
            opponent_sign = 'o'        ####Change-1
        else:
            opponent_sign = 'x'

        if depth == itr_max_depth:
            return (self.utility_get(board,player_sign,opponent_sign), best_row, best_coloumn)  ####Change-3
        else:
            available_moves = board.find_valid_move_cells(old_move)

            if len(available_moves) == 0:       ##### No moves left at depth
                return (self.utility_get(board, player_sign, opponent_sign), best_row, best_coloumn)  ###Change-4(though same)

            if depth == 0:      #If at first level we have around 56 cells then decrease level by 1
                if len(available_moves) > 17:
                    self.MaxDepth = min(self.MaxDepth, 2)

            for move in available_moves:  # assign player sign whose turn is this
                temp_board = copy.deepcopy(board)

                cntp_1 = sum(blocks.count(player_sign) for blocks in temp_board.block_status)
                cnto_1 = sum(blocks.count(opponent_sign) for blocks in temp_board.block_status)



                if node_type_maxnode:
                    temp_board.update(old_move, move, player_sign)
                else:
                    temp_board.update(old_move, move, opponent_sign)

                cntp_2 = sum(blocks.count(player_sign) for blocks in temp_board.block_status)
                cnto_2 = sum(blocks.count(opponent_sign) for blocks in temp_board.block_status)
                if self.win_move == True:
                    self.win_move = False

                elif cntp_1 + 1 == cntp_2:
                    self.win_player = player_sign
                    self.win_move = True
                    self.win_once_flag = True

                elif cnto_1 + 1  == cnto_2:
                    self.win_player = opponent_sign
                    self.win_move = True
                    self.win_once_flag = True

                node_type_maxnode1 = node_type_maxnode

                if self.win_move == False:
                    if node_type_maxnode==True:
                        node_type_maxnode1 = False
                    else:
                        node_type_maxnode1 = True

                utility = self.MinMax(temp_board, move, node_type_maxnode1, player_sign, depth+1 , alpha, beta, best_row, best_coloumn, itr_max_depth,st_time) # agains call MinMax
                if node_type_maxnode:  #Rules for PRUNING
                    if utility[0] > alpha:
                        alpha = utility[0]
                        best_row = move[0]
                        best_coloumn = move[1]
                else:  # Rules for PRUNING """
                    if utility[0] < beta:
                        beta = utility[0]
                        best_row = move[0]
                        best_coloumn = move[1]

                if alpha >= beta: # Rules for PRUNING """
                    break;

                if (time.time() - st_time)>15:
                    return (utility, best_row, best_coloumn)

            if node_type_maxnode:
                return (alpha, best_row, best_coloumn)
            else:
                return (beta, best_row, best_coloumn)

    def move(self, board, old_move, player_flag):
        if old_move == (-1, -1):
            return (4, 4)
        startt = time.time()
        if player_flag == 'o':
            flag2 = 'x'
        else:
            flag2 = 'o'
        self.cntp = 0
        self.cnto = 0
                                                ####Change-5
        for blocks in board.block_status:
            #for block in blocks:
            if blocks == player_flag:
                self.cntp += 1
            if blocks == flag2:
                self.cnto += 1


        self.temp_board = copy.deepcopy(board)
        #self.temp_block = copy.deepcopy(board.block_status)

        temp_move = (0,0,0)
        itr_max_depth = 3##CHANGE D
        inv_move = (-1,-1)
        while(time.time() - startt < 15):       ####Change-2
            next_move = temp_move
            temp_move = self.MinMax(self.temp_board, old_move, True, player_flag, 0, -100000000000000.0, 10000000000000.0, -1,
                                     -1, itr_max_depth,startt)
            itr_max_depth += 1
            elapsed = (time.time() - startt)
        return (next_move[1], next_move[2])

    def get_factor(self, p_gain, gain):####NEED CHANGES HERE
        if p_gain <= 0:
            if p_gain >= -1 and p_gain <= 0 :
                gain += p_gain
            elif p_gain < -1 and p_gain >= -2:
                val = -1
                val -= (abs(p_gain) - 1) * 9
                gain += val
            if p_gain >= -3 and p_gain < -2:
                val = -10
                val -= (abs(p_gain) - 2) * 90
                gain += val
            elif p_gain < -3 and p_gain >= -4:
                val = -100
                val -= (abs(p_gain) - 3) * 900
                gain += val
            if p_gain < -4:
                val = -1000
                val -= (abs(p_gain) - 4) * 9000
                gain += val
        else:
            if p_gain > 0 and p_gain < 1:
                gain += p_gain
            elif p_gain >= 1 and p_gain < 2:
                val = 1
                val += (p_gain - 1) * 9
                gain += val

            elif p_gain >= 2 and p_gain < 3:
                val = 10
                val += (p_gain - 2) * 90
                gain += val
            elif p_gain>= 3 and p_gain < 4:
                val = 100
                val += (p_gain - 3) * 900
                gain += val
            elif p_gain >= 4:
                val = 1000
                val += (p_gain - 4) * 9000
                gain += val
        return gain



    def straight_utility(self,board,playerFlag,opFlag,gain,utility_values_block,sig):
        if sig == 'c':
            for i in range(4):#col blocks
                p = 0
                curr = 0
                oppo = 0
                for j in range(4):
                    p += utility_values_block[j * 4 + i]
                    if board.block_status[j][i] == playerFlag:
                        curr += 1
                    elif board.block_status[j][i] == opFlag:
                        oppo += 1
                gain = self.get_factor(p, gain)
                gain +=  10*self.Util_Matrix[curr][oppo]#*self.blockWts[j][i]

        elif sig == 'r':
                for j in range(4):#row blocks
                    p = 0
                    curr = 0
                    oppo = 0
                    for i in range(4):
                        p += utility_values_block[j * 4 + i]
                        if board.block_status[j][i] == playerFlag:
                            curr += 1
                        elif board.block_status[j][i] == opFlag:
                            oppo += 1
                    gain = self.get_factor(p, gain)
                    gain +=  10*self.Util_Matrix[curr][oppo]
        return gain

    def diamond_utility(self,board,playerFlag,opFlag,gain,utility_values_block):
        counter = 0
        for i in range(2):
            for j in range(2):
                empty = 0
                p = 0
                curr = 0
                oppo = 0
                if board.block_status[i][1+j] == '-':
                    empty +=1
                elif board.block_status[i][1+j] == playerFlag:
                    curr +=1
                else:
                    oppo +=1

                if board.block_status[1+i][1-1+j] == '-':
                    empty +=1
                elif board.block_status[1+i][1-1+j] == playerFlag:
                    curr +=1
                else:
                    oppo +=1

                if board.block_status[2+i][1+j] == '-':
                    empty +=1
                elif board.block_status[2+i][1+j] == playerFlag:
                    curr +=1
                else:
                    oppo +=1

                if board.block_status[1+i][1+1+j] == '-':
                    empty+=1
                elif board.block_status[1+i][1+1+j] == playerFlag:
                    curr +=1
                else:
                    oppo +=1

                if counter==0:
                    p += utility_values_block[1] + utility_values_block[4] + utility_values_block[9] + utility_values_block[6]
                elif counter == 1:
                    p += utility_values_block[2] + utility_values_block[5] + utility_values_block[10] + utility_values_block[7]
                elif counter == 2:
                    p += utility_values_block[5] + utility_values_block[8] + utility_values_block[10] + utility_values_block[13]
                else:
                    p += utility_values_block[6] + utility_values_block[9] + utility_values_block[11] + utility_values_block[14]

                gain = self.get_factor(p, gain)
                gain +=  10*self.Util_Matrix[curr][oppo]
                #gain = self.calculate(curr, oppo, gain,1)
                counter += 1
        return gain

    def utility_get(self, board, playerFlag, opFlag):

        utility_values_block = [0 for i in range(16)]

        for i in range(16):
            utility_values_block[i] = self.calc_utility(board, i, playerFlag)/1000.0
        #utlitiy of each of the blocks

        gain = 0

        gain = self.straight_utility(board,playerFlag,opFlag,gain,utility_values_block,'c')

        gain = self.straight_utility(board,playerFlag,opFlag,gain,utility_values_block,'r')

        gain = self.diamond_utility(board,playerFlag,opFlag,gain,utility_values_block)

        cnt1 = 0
        cnt2 = 0
        for blocks in board.block_status:
            for s in blocks:
                if s == playerFlag:
                    cnt1 += 1
                elif s == opFlag:
                    cnt2 += 1
        if self.cntp < cnt1 and cnt2 == self.cnto:
            gain += 50
        elif cnt2 > self.cnto and (cnt1 - self.cntp) > (cnt2 - self.cnto):
            gain += 20
        elif cnt1 > self.cntp and (cnt1 - self.cntp) < (cnt2 - self.cnto):
            gain -= 20
        elif cnt1 >= self.cntp and cnt2 > self.cnto:
            gain -= 50
        return gain

    def straight_calc(self,board,startx,starty,playerFlag,gain,fl):
        if fl == 'r':
            for i in range(startx, startx + 4):#within block rows
                curr = 0
                oppo = 0
                neutral = 0
                for j in range(starty, starty + 4):
                    if board.board_status[i][j] == '-':
                        neutral += 1
                    elif board.board_status[i][j] == playerFlag:
                        curr += 1
                    else:
                        oppo += 1
                gain +=  self.Util_Matrix[curr][oppo]

        elif fl == 'c':
            for j in range(starty, starty + 4):
                curr = 0
                oppo = 0
                neutral = 0
                for i in range(startx, startx + 4):
                    if board.board_status[i][j] == '-':
                        neutral += 1
                    elif board.board_status[i][j] == playerFlag:
                        curr += 1
                    else:
                        oppo += 1
                gain +=  self.Util_Matrix[curr][oppo]
        return gain

    def diamond_calc(self,board,startx,starty,playerFlag,gain):
        for i in range(2):
            for j in range(2):
                empty = 0
                p = 0
                empty = 0
                curr = 0
                oppo = 0

                if board.board_status[startx + i][starty + 1+j] == '-':
                    empty +=1
                elif board.board_status[startx + i][starty + 1+j] == playerFlag:
                    curr +=1
                else:
                    oppo +=1

                if board.board_status[startx + 1+i][starty + 1-1+j] == '-':
                    empty +=1
                elif board.board_status[startx + 1+i][starty + 1-1+j] == playerFlag:
                    curr +=1
                else:
                    oppo +=1

                if board.board_status[startx + 2+i][ starty + 1+j] == '-':
                    empty+=1
                elif board.board_status[startx + 2+i][ starty + 1+j] == playerFlag:
                    curr+=1
                else:
                    oppo +=1

                if board.board_status[startx + 1+i][starty + 1+1+j] == '-':
                    empty+=1
                elif board.board_status[startx + 1+i][starty + 1+1+j] == playerFlag:
                    curr+=1
                else:
                    oppo +=1

                gain +=  self.Util_Matrix[curr][oppo]####MULTIPLY BY 2..................#####

        return gain


    def calc_utility(self, board, boardno, playerFlag):

        gain = 0
        startx = boardno / 4
        starty = boardno % 4
        startx *= 4
        starty *= 4

        gain = self.straight_calc(board,startx,starty,playerFlag,gain,'r')

        gain = self.straight_calc(board,startx,starty,playerFlag,gain,'c')

        gain = self.diamond_calc(board,startx,starty,playerFlag,gain)

        pf = playerFlag
        if playerFlag == 'x':
            of = 'o'
        else:
            of = 'x'

        i = 0
        j = 0
        tempx = 0
        tempy  = 0
        for lineh in self.horizontal:
            for linev in self.vertical:
                cntph = 0
                cntoh = 0
                cntpv = 0
                cntov = 0
                for point in lineh:
                    tempx = point[0]
                    if board.board_status[startx+point[0]][starty+point[1]] == pf:
                        cntph += 1
                    elif board.board_status[startx+point[0]][starty+point[1]] == of:
                        cntoh += 1

                for point in linev:
                    tempy = point[1]
                    if board.board_status[startx+point[0]][starty+point[1]] == pf:
                        cntpv += 1
                    elif board.board_status[startx+point[0]][starty+point[1]] == of:
                        cntov += 1

                if cntov==0 and cntph==0:
                    if cntoh==2 and cntpv==3 and board.board_status[startx+tempx][starty+tempy]==pf:
                        gain += 10

                if cntpv==0 and cntoh==0:
                    if cntph==3 and cntov==2 and board.board_status[startx+tempx][starty+tempy]==pf:
                        gain += 10
        return gain
