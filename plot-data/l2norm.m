function s = l2norm(output_file,varargin);
fig = figure;
hold all;
set(gcf,'PaperPositionMode','auto');
L = {}; %holds the legend names
for k = 1:2:length(varargin)-1
    Yk = dlmread(varargin{k});
    Xk = [1 : length(Yk) ]';
    plot(Xk,Yk,'LineWidth',1.0)
    j = floor(k/2)+1;
    L{j} = varargin{k+1};
end
leg = legend(L);
set(leg,'FontSize',20);
xlabel('Review');
ylabel('L2 Norm');
print(fig, output_file,'-dpng');