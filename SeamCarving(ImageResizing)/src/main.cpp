#include <iostream>
#include <fstream>
#include <math.h>
using namespace std;

double gradientCalculate(int ***rgb,int H,int W,int C,int row,int col){
    int x1[]= { col-1>=0 ? rgb[row][col-1][0] : rgb[row][W-1][0], col-1>=0 ? rgb[row][col-1][1] : rgb[row][W-1][1], col-1>=0 ? rgb[row][col-1][2] : rgb[row][W-1][2]};
    int x2[]= { col+1<W ? rgb[row][col+1][0] : rgb[row][0][0], col+1<W ? rgb[row][col+1][1] : rgb[row][0][1], col+1<W ? rgb[row][col+1][2] : rgb[row][0][2]};
    int y1[]= { row-1>=0 ? rgb[row-1][col][0] : rgb[H-1][col][0] , row-1>=0 ? rgb[row-1][col][1] : rgb[H-1][col][1], row-1>=0 ? rgb[row-1][col][2] : rgb[H-1][col][2]};
    int y2[]= { row+1<H ?rgb[row+1][col][0] : rgb[0][col][0], row+1<H ?rgb[row+1][col][1] : rgb[0][col][1], row+1<H ?rgb[row+1][col][2] : rgb[0][col][2]};

    int deltaX = (x2[0]-x1[0])*(x2[0]-x1[0]) + (x2[1]-x1[1])*(x2[1]-x1[1]) + (x2[2]-x1[2])*(x2[2]-x1[2]);
    int deltaY = (y2[0]-y1[0])*(y2[0]-y1[0]) + (y2[1]-y1[1])*(y2[1]-y1[1]) + (y2[2]-y1[2])*(y2[2]-y1[2]);

    double gradient = sqrt(deltaX+deltaY);
    return gradient;
}
double** computeGradientMatrix(int ***rgb,int H,int W,int C){
    double** gradientMatrix;
    gradientMatrix = new double *[H];
    for(int i=0;i<H;i++){
        gradientMatrix[i] = new double [W];
        for(int j=0;j<W;j++){
            gradientMatrix[i][j] = gradientCalculate(rgb,H,W,C,i,j);
        }
    }
    return gradientMatrix;
}

void solve(int ***rgb, int H, int W, int C, int H_, int W_, int C_) {
    // We've provided you the driver.py and main.cpp for your convinience
    // Please go through them and understand the file handling and input/output format
    // Feel free to experiment on your own
    // can access the array using rgb[i][j][k] like a regular 3D array
    // Write your code here
    
    //Removing Vertical Seam first->Reduces Width
    while(W>W_){
        double** gradientMatrix = computeGradientMatrix(rgb,H,W,C);
        double** dp = new double *[H];
        dp[0] = new double[W];
        for(int i=0;i<W;i++){
            dp[0][i]=gradientMatrix[0][i];
        }
        for(int i=1;i<H;i++){
            dp[i] = new double[W];
            for(int j=0;j<W;j++){
                dp[i][j]= dp[i-1][j];
                if(j-1>=0){
                    dp[i][j] = min(dp[i][j],dp[i-1][j-1]);
                }
                if(j+1<W){
                    dp[i][j] = min(dp[i][j],dp[i-1][j+1]);
                }
                dp[i][j]+=gradientMatrix[i][j];
            }
        }
        double maxSeam;
        int maxIndex,index;
        maxSeam = dp[H-1][0];
        maxIndex=0;
        for(int j=0;j<W;j++){
            if(maxSeam>dp[H-1][j]){
                maxSeam = dp[H-1][j];
                maxIndex=j;
            }
        }
        for(int i=maxIndex;i<W-1;i++){
            rgb[H-1][i][0]=rgb[H-1][i+1][0];    
            rgb[H-1][i][1]=rgb[H-1][i+1][1];  
            rgb[H-1][i][2]=rgb[H-1][i+1][2];  
        }
        
        for(int i=H-2;i>=0;i--){
            maxSeam = dp[i][maxIndex];
            index=maxIndex;
            if(index-1>=0 && maxSeam > dp[i][index-1]){
                maxSeam=dp[i][index-1];
                maxIndex = index-1; 
            }
            if(index+1<W && maxSeam > dp[i][index+1]){
                maxSeam = dp[i][index+1];
                maxIndex=index+1;
            }
            for(int j=maxIndex;j<W-1;j++){
                rgb[i][j][0]=rgb[i][j+1][0];    
                rgb[i][j][1]=rgb[i][j+1][1];  
                rgb[i][j][2]=rgb[i][j+1][2];  
            }
            
        }
        W--;
    }

    //Removing Horizontal Seam first->Reduces Height
    while(H>H_){
        double** gradientMatrix = computeGradientMatrix(rgb,H,W,C);

        double** dp = new double *[H];
        for(int i=0;i<H;i++){
            dp[i]=new double[W];
        }

        for(int i=0;i<H;i++){
            dp[i][0]=gradientMatrix[i][0];
        }

        for(int j=1;j<W;j++){
            for(int i=0;i<H;i++){
                dp[i][j]= dp[i][j-1];
                if(i-1>=0){
                    dp[i][j] = min(dp[i][j],dp[i-1][j-1]);
                }
                if(i+1<H){
                    dp[i][j] = min(dp[i][j],dp[i+1][j-1]);
                }
                dp[i][j]+=gradientMatrix[i][j];
            }
        }
        
        double maxSeam;
        int maxIndex,index;
        maxSeam = dp[0][W-1];
        maxIndex=0;
        
        for(int i=0;i<H;i++){
            if(maxSeam>dp[i][W-1]){
                maxSeam = dp[i][W-1];
                maxIndex=i;
            }
        }
        for(int i=maxIndex;i<H-1;i++){
            rgb[i][W-1][0]=rgb[i+1][W-1][0];
            rgb[i][W-1][1]=rgb[i+1][W-1][1];
            rgb[i][W-1][2]=rgb[i+1][W-1][2];
        }
        for(int j=W-2;j>=0;j--){
            maxSeam = dp[maxIndex][j];
            index=maxIndex;
            if(index-1>=0 && maxSeam > dp[index-1][j]){
                maxSeam=dp[index-1][j];
                maxIndex = index-1; 
            }
            if(index+1<H && maxSeam > dp[index+1][j]){
                maxSeam = dp[index+1][j];
                maxIndex= index+1;
            }

            for(int i=maxIndex;i<H-1;i++){
                rgb[i][j][0]=rgb[i+1][j][0];
                rgb[i][j][1]=rgb[i+1][j][1];
                rgb[i][j][2]=rgb[i+1][j][2];
            }

            
        }
        H--;
    }
    

}

int main() {
    string ip_dir = "./data/input/";
    string ip_file = "rgb_in.txt";
    ifstream fin(ip_dir + ip_file);

    int H, W, C;
    fin >> H >> W >> C;

    int ***rgb;
    rgb = new int **[H];
    for(int i = 0; i < H; ++i) {
        rgb[i] = new int *[W];
        for(int j = 0; j < W; ++j) {
            rgb[i][j] = new int[C];
            for(int k = 0; k < C; ++k)
                fin >> rgb[i][j][k];
        }
    }
    fin.close();

    int H_, W_, C_;
    cout << "Enter new value for H (must be less than " << H << "): ";
    cin >> H_;
    cout << "Enter new value for W (must be less than " << W << "): ";
    cin >> W_;
    cout << '\n';
    C_ = C;

    solve(rgb, H, W, C, H_, W_, C_);

    string op_dir = "./data/output/";
    string op_file = "rgb_out.txt";
    ofstream fout(op_dir + op_file);
    

    fout << H_ << " " << W_ << " " << C_ << endl;
    for(int i = 0; i < H_; ++i) {
        for(int j = 0; j < W_; ++j) {
            for(int k = 0; k < C_; ++k) {
                fout << rgb[i][j][k] << " ";
            }
        }
        fout << '\n';
    }
    fout.close();

    return 0;
}