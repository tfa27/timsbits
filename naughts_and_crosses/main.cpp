#include <iostream>
#include <cmath>
#include <vector>
#include <stdlib.h>

class Board{
private:
    std::vector <std::vector<int>> vec {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
public:
    void display_board();
    void update_board_player(int r, int c, int play);
    void update_board_comp(int &steps);
    void reset();
    bool check_done();
};

int main(){
    Board board;
    std::cout << rand() % 3 << "\n";
    int steps {0};
    bool done {0};
    while (!done){
	    board.display_board();
        double location;
        std::cout << "Enter location to go, in the format 1.1 (i.e. first row, first column, to 3.3, third row, third column (row.col)): ";
        std::cin >> location;
        int row {static_cast<int>(round(location))};
        double remainder {((location - row)*10)+0.5};
        int col {static_cast<int>(remainder)};
        std::cout << "Row: " << row << " | Col: " << col << "\n";
        board.update_board_player(row, col, 1);
        board.update_board_comp(steps);
        std::cout << "\n\n";
        done = board.check_done();
    }
    board.display_board();
    std::cout << "\n\nDraw! Thanks for playing!\n";
	return 0;
}

void Board::display_board(){
    std::vector <char> options {' ', 'X', 'O'};
    for (int i {0}; i < 3; i++){
        for (int j {0}; j < 3; j++){
            char this_char {options.at(vec.at(i).at(j))};
            std::cout << "[" << this_char << "]";
            if (j != 2){
                std::cout << "-";
            }
        }
        std::cout << "\n";
    }
}

void Board::update_board_player(int r, int c, int play){
    r -= 1;
    c -= 1;
    if (vec.at(r).at(c) == 0){
        vec.at(r).at(c) = play;
    }
}

void Board::update_board_comp(int &steps){
    bool full_done {0};
    while (!full_done){
        if (steps == 0){
            bool this_done {0};
            while (!this_done){
                if (vec.at(1).at(1) == 0 ){
                    update_board_player(2, 2, 2);
                    full_done = 1;
                    this_done = 1;
                }
                int r {rand() % 3};
                if (r != 1){
                    if (vec.at(r).at(r) != 1){
                        update_board_player(r+1, r+1, 2);
                        this_done = 1;
                        full_done = 1;
                    }
                }
            }
        } else {
            int this_row {0};
            for (int row {0}; row < 3; row++){
                int row_count {0};
                for (int col {0}; col < 3; col++){
                    if (vec.at(row).at(col) == 1){
                        row_count += 1;
                        this_row = row;
                    }
                }
                if (row_count == 2){
                    for (int col {0}; col < 3; col++){
                        if (vec.at(row).at(col) == 0){
                            update_board_player(this_row+1, col + 1, 2);
                            full_done = 1;
                        }
                    }
                }
            }
            int this_col {0};
            for (int col{0}; col < 3; col++){
                int col_count {0};
                for (int row{0}; row < 3; row++){
                    if (vec.at(row).at(col) == 1){
                        col_count += 1;
                        this_col = col;
                    }
                }
                if (col_count == 2){
                    for (int row {0}; row < 3; row++){
                        if (vec.at(row).at(col) == 0){
                            update_board_player(row+1, this_col + 1, 2);
                            full_done = 1;
                        }
                    }
                }
            }
            // diagonal section fuck me this code is a mess but if it
            // works I'll shove it up my arse
            int row{0};
            int col {0};
            int diag_one_ctr {0};
            while (row < 3 && col < 3){
                if (vec.at(row).at(col) == 1){
                    diag_one_ctr += 1;
                } else if (vec.at(row).at(col) == 2){
                    diag_one_ctr -= 1;
                }
                row += 1;
                col += 1;
            }
            if (diag_one_ctr == 2){
                int row{0};
                int col {0};
                while (row < 3 && col < 3){
                    if (vec.at(row).at(col) == 0){
                        update_board_player(row+1, col + 1, 2);
                        full_done = 1;
                    }
                    row += 1;
                    col += 1;
                }
            }
            int diag_back_ctr {0};
            row = 2;
            col = 0;
            while (col < 3 && row >= 0){
                if (vec.at(row).at(col) == 1){
                    diag_back_ctr += 1;
                } else if (vec.at(row).at(col) == 2){
                    diag_back_ctr -= 1;
                }
                row -= 1;
                col += 1;
            }
            if (diag_back_ctr == 2){
                int row {2};
                int col {0};
                while (col < 3 && row >= 0){
                    if (vec.at(row).at(col) == 0){
                        update_board_player(row+1, col + 1, 2);
                        full_done = 1;
                    }
                    row -= 1;
                    col += 1;
                }
            }
        }
        if (full_done != 1){
                bool another_done {0};
                while (!another_done){
                    int r_row {rand() % 3};
                    int r_col {rand() % 3};
                    if (vec.at(r_row).at(r_col) == 0){
                        update_board_player(r_row+1, r_col+1, 2);
                        full_done = 1;
                        another_done = 1;
                    }
                }
            }
    }
    steps += 1;
}

void Board::reset(){
    for (int r {0}; r < 3; r++){
        for (int c {0}; c < 3; c++){
            vec.at(r).at(c) = 0;
        }
    }
}

bool Board::check_done(){
    int done_count {0};
    bool full_done {0};
    for (int row {0}; row < 3; row++){
        for (int col {0}; col < 3; col ++){
            if (vec.at(row).at(col) == 0){
                done_count += 1;
            }
        }
    }
    if (done_count == 1){
            full_done = 1;
        }
    return full_done;
}