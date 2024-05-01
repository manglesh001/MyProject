#include <iostream>
#include <string>
#include <unistd.h>
#include <sys/types.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sstream>
#include <fcntl.h>
#include <ctime>
#include <pwd.h>
#include <libgen.h> 
#include <grp.h>
#include <sys/wait.h>
#include <cstring>
#include <vector>
#include <sstream>
#include <cstdlib>
using namespace std;
void Display() 
{
char user[50];
getlogin_r(user,sizeof(user));
char host[50];
gethostname(host,sizeof(host));    
char cdir[50];
getcwd(cdir,sizeof(cdir));
string homedir(getenv("HOME"));
string cwd(cdir);
if(cwd.find(homedir)==0) 
cwd.replace(0,homedir.length(),"~");
cout<<user<<"@";
cout<<host<<":";
cout<<cwd<<">";
}
bool searchDir(string& target,string& currdir) 
{
struct stat st;
string name;
dirent* e;
DIR* dir;
dir=opendir(currdir.c_str());
if(!dir){
return false;
}
while((e=readdir(dir))) 
{
name=e->d_name;
if(name=="."||name=="..")
continue; 
string path=currdir+"/"+name;
if(stat(path.c_str(),&st)==-1)
continue; 
if(name==target) 
{
closedir(dir);
return true; 
}
if(S_ISDIR(st.st_mode))
{
if(searchDir(target,path))
{
closedir(dir);
return true;
}
}
}
closedir(dir);
return false;
}
bool changeDir(string& input,char* prevdir)
{
char* pd;
if(input==".") 
return true;
else if(input == "..") 
{
pd=dirname(prevdir);
if(chdir(pd)!= 0)
return false;
}
else if(input=="~")
{
char* home=getenv("HOME");
if(home==nullptr)
return false;
if(chdir(home)!=0)
return false;
}
else if(input=="-")
{
prevdir=getenv("OLDPWD");
if(prevdir!=nullptr) {
if(chdir(prevdir)==0)
{
return true;
}
}}
else if(input[0]=='/')
{
string s=input.substr(1,input.length());
if(chdir(s.c_str()) != 0)
return false;
}
else
{
if(chdir(input.c_str())!=0)
return false;
} 
    return true;
}
void ls(vector<string>& tokens)
{
long total=0;
char dates[50];
bool lf=false;
vector<string> files;
bool hd=false;
for(int i=1;i<tokens.size();i++)
{
string &arg=tokens[i];
if(arg=="-al"||arg=="-la")
{
hd=true;
lf=true;
}
else if(arg=="-a")
hd=true;
else if(arg=="-l") 
lf=true;
else if(arg[0]!='-') 
files.push_back(arg);
}
if(files.empty())
files.push_back(".");
for(string& s:files) 
{
struct dirent* e;
DIR* dir=opendir(s.c_str());
if(dir)
{
while((e=readdir(dir)))
{
if(!hd && e->d_name[0]=='.')
continue;
struct stat st;
if(stat((s+"/"+e->d_name).c_str(),&st)==0)
total=total+st.st_blocks;
else
cerr<<"Error FileStat"<<endl;
}
if(lf==true)
cout<<"Total:"<<total/2<<endl;
rewinddir(dir);
while((e=readdir(dir)))
{
if(!hd && e->d_name[0]=='.')
continue;
struct stat st;
if(stat((s+"/"+e->d_name).c_str(),&st)==0){
if(lf==true)
{
if(S_ISDIR(st.st_mode))
cout<<"d";
else
cout<<"-";
if(st.st_mode & S_IRUSR)
cout<<"r";
else
cout<<"-";
if(st.st_mode & S_IWUSR)
cout<<"w";
else
cout<<"-";
if(st.st_mode & S_IXUSR)
cout<<"x";
else
cout<<"-";
if(st.st_mode & S_IRGRP)
cout<<"r";
else
cout<<"-";
if(st.st_mode & S_IWGRP)
cout<<"w";
else
cout<<"-";
if(st.st_mode & S_IXGRP)
cout<<"x";
else
cout<<"-";
if(st.st_mode & S_IROTH)
cout<<"r";
else
cout<<"-";
if(st.st_mode & S_IWOTH)
cout<<"w";
else
cout<<"-";
if(st.st_mode & S_IXOTH)
cout<<"x";
else
cout<<"-";
cout<<" "<<st.st_nlink;
struct passwd* password=getpwuid(st.st_uid);
struct group* grp=getgrgid(st.st_gid);
cout<<" "<<password->pw_name;
cout<<" "<<grp->gr_name;
cout<< " "<<st.st_size;
strftime(dates,sizeof(dates),"%b %d %H:%M",localtime(&st.st_mtime));
cout<<" "<<dates;
cout<<" "<<e->d_name<<endl;
}
else 
{
cout<<e->d_name<<" ";
}
}}
cout<<endl;
closedir(dir);
}
else
cerr<<"File or Directories is not Found"<<endl;
}
}
void background(vector<string> & token)
{
int n=token.size();
char* ch[n+1];
for(int i=0;i<n;i++) 
ch[i]=const_cast<char*>(token[i].c_str());

ch[n]=nullptr;
pid_t cpid=fork();
if(cpid>0)
cout<<cpid<<endl;
else if(cpid==0) 
{
if(execvp(ch[0],ch)==-1)
{
cerr<<ch[0]<<" Command Not Found"<< endl;
exit(1);
}
}
else
{
cerr<<"Child Process Failed To Create"<< endl;
exit(1);
}
}
void Print(vector<string>& tokens) 
{
for(int i=1;i<tokens.size();i++)
cout<<tokens[i]<<" ";
cout<<endl;
}
void Processinfo(vector<string>& tokens) 
{
char sf[200];
char line[200];
string ps;
char ex[200];
char mf[100];
unsigned long vm;
int pid;
if(tokens.size()==1)
pid=getpid();
else if(tokens.size()==2)
pid=stoi(tokens[1]);
else
{
cerr<<"Process Information Invalid Arguments"<<endl;
return;
}
snprintf(sf,sizeof(sf),"/proc/%d/status",pid);
snprintf(mf,sizeof(mf),"/proc/%d/statm",pid);
FILE* f=fopen(sf,"r");
f=fopen(mf,"r");
snprintf(ex,sizeof(ex),"/proc/%d/exe",pid);
int len=readlink(ex,ex,sizeof(ex)-1);
if(!f || fscanf(f,"%lu",&vm)!=1 || len==-1)
{
cerr<<"This Process is NOT running"<<endl;
return;
}
if(len!=-1)
ex[len]='\0';
fclose(f);
cout<<"Pid-"<<pid<<endl;
cout<<"Process Status-"<<ps<<endl;
cout<<"Memory-" <<vm<<"{Virtual Memory}"<<endl;
cout<<"Executable Path-"<<ex<<endl;
}
void Checkdir()
{
char cwd[150];
getcwd(cwd,sizeof(cwd));
cout<<cwd<<endl;
}
int main()
{
string input;
while(true)
{
Display();
if(!getline(cin,input))
exit(1);

vector<string> token;
char prevDir[150];
char* t=strtok(const_cast<char*>(input.c_str())," ");
if(getcwd(prevDir,sizeof(prevDir))==nullptr){
cerr<<"not found previous working directory"<<endl;        
}
while(t!=nullptr)
{
token.push_back(string(t));
t=strtok(nullptr," ");
}
if(!token.empty()) 
{
if(token.back()=="&")
{
token.pop_back();
background(token);
}
else if(token[0]=="cd")
{
if(token.size()==1)
{
char* home=getenv("HOME");
if(home==nullptr) 
return false;
if(chdir(home)!= 0)
{
cerr<<"Error in Changing Directory"<<endl;
return false;
}
}
else{
string path=token[1];
bool flag=changeDir(path,prevDir);
if(!flag)
cerr<<"Error in Changing Directory"<<endl;
}}
else if(token[0]=="exit")
{
break;
}
else if(token[0]=="ls")
{
ls(token);
}
else if(token[0]=="echo")
{
Print(token);
}
else if(token[0]=="pwd")
{
Checkdir();
}
else if(token[0]=="search")
{
if(token.size()!=2) {
cerr<<"Search give one more arguments"<<endl;
}
else 
{
string t=token[1];
string cdir;
char cwd[100];
if(getcwd(cwd,sizeof(cwd))) 
{
cdir=cwd;
bool result=searchDir(t,cdir);
cout<<(result?"True":"False")<<endl;
} 
else
{
cerr<<"Error getting current directory"<<endl;
}
}
}
else if(token[0]=="pinfo") 
{
Processinfo(token);
}
else{
cout<<"Command not Found"<<endl;
}
}
}
return 0;
}

