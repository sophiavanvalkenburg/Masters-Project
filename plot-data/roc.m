function r = roc(output_file,varargin);
fig = figure;
hold all;
set(gcf,'PaperPositionMode','auto');
L = {}; %holds the legend names
for i = 1:3:length(varargin)-1
    M = dlmread(varargin{i},',');
    fpr = M(:,2);
    tpr = M(:,1);
    linestyle = varargin{i+2};
    plot(fpr,tpr,linestyle,'LineWidth',2.0);
    k = floor(i/3)+1; %legend name
    L{k} = varargin{i+1};
end
R = [0:10]'/10;
plot(R,R,'k','LineWidth',2.0)
L{end+1} = 'Random';
leg = legend(L,'Location','SouthEast');
set(leg,'FontSize',8);
xlabel('FPR');
ylabel('TPR');
print(fig, output_file,'-dpng');