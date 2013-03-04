function s = sv_binary_real(bin_file, real_file,output_file)
Yb = dlmread(bin_file)
Yr = dlmread(real_file)
Xb = [1 : length(Yb)]'
Xr = [1 : length(Yr)]'
fig = figure
set(gcf,'PaperPositionMode','auto')
plot(Xb,Yb,'b',Xr,Yr,'r','LineWidth',2.0)
leg = legend('binary-valued','real-valued','Location','East')
set(leg,'FontSize',50)
print(fig, output_file,'-dpng')