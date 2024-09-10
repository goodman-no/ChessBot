from utils import NEGATIVE_INF, INF

class Evaluation:
    def __init__(self, eval, move):
        self.eval = eval
        self.move = move

class Engine:
    def __init__(self):
        pass

    def evaluate(self, board):
        current_total = 0
        opponent_total = 0

        for row in board.squares:
            for square in row:
                if square.is_white == board.white_turn:
                    current_total += square.get_value()
                elif not square.is_empty():
                    opponent_total += square.get_value()
        
        return current_total - opponent_total
    
    def depth_1_best_move(self, board):
        moves = board.generate_legal_moves()

        best_move = Evaluation(NEGATIVE_INF, None)
        for move in moves:
            test_position = board.test(move)
            responses = test_position.generate_legal_moves()
            worst_response = Evaluation(NEGATIVE_INF, None)
            for response in responses:
                response_test_position = test_position.test(response)
                response_evaluation = -self.evaluate(response_test_position)
                if response_evaluation > worst_response.eval:
                    worst_response = Evaluation(response_evaluation, response)
                
                #print(f"Caluclated {-response_evaluation} Line: {move.to_str()} --> {response.to_str()}")
            if -worst_response.eval > best_move.eval:
                best_move = Evaluation(-worst_response.eval, move)
        
        #print(f"Best Line: {best_move.eval} : {best_move.move.to_str()}")
        return best_move
    
    def depth_best_move(self, board, depth):
        if depth == 0:
            return self.evaluate(board)

        best_move = NEGATIVE_INF
        for move in board.generate_legal_moves():
            test_position = board.test(move)
            next_best_move = self.depth_best_move(test_position, depth - 1)
            if next_best_move > best_move:
                best_move = next_best_move
        
        return best_move

    def best_move_search(self, board, depth):
        moves = board.generate_legal_moves()

        max_eval = self.depth_best_move(board.test(moves[0]), depth)
        max_move = moves[0]

        for i, move in enumerate(moves):
            print(f"CHECKED MOVE {i + 1}/{len(moves)}")
            move_eval = self.depth_best_move(board.test(move), depth)
            if move_eval > max_eval:
                max_eval = move_eval
                max_move = move
        
        print(f"EVAL: {max_eval}, MOVE: {max_move.to_str()}")
        return max_move

        



