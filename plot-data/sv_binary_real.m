function s = sv_binary_real(output_file,bin_file,real_file)
fig = figure
set(gcf,'PaperPositionMode','auto')
Yb = dlmread(bin_file)
Xb = [1 : length(Yb) ]'
Yr = dlmread(real_file)
Xr = [1 : length(Yr) ]'
plot(Xb,Yb,'b',Xr,Yr,'r','LineWidth',2.0)
leg = legend('binary-valued','real-valued','Location','East')
set(leg,'FontSize',50)
print(fig, output_file,'-dpng')