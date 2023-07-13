
library(viridis)
library(rstan)
library(rgl)
library(RColorBrewer)
library(brms)
library(rstanarm)
library(geoR)
library(lattice)
library(aqfig)
library(fields)
library(colorRamps)


#################################################
##### Application to the Leukemia dataset #######
#################################################


leukemia <- read.table(".../leukemia.txt", header = TRUE)

summary(leukemia)
str(leukemia)

# transform white blood cell count (wbc), which has highly skewed distribution with zeros for measurements below measurement accuracy
leukemia$wbc <- log10(leukemia$wbc + 0.3)

# normalize continuous covariates 
leukemia$age <- scale(leukemia$age, scale=TRUE, center=TRUE)
leukemia$wbc <- scale(leukemia$wbc, scale=TRUE, center=TRUE)
leukemia$tdi <- scale(leukemia$tdi, scale=TRUE, center=TRUE)
leukemia$log_time <- scale(log(leukemia$time), scale=FALSE, center=TRUE)

# mean and std of original covariates
m_time <- attr(leukemia$log_time,"scaled:center")
sd_age <- attr(leukemia$age,"scaled:scale")
m_age <- attr(leukemia$age,"scaled:center")
sd_wbc <- attr(leukemia$wbc,"scaled:scale")
m_wbc <- attr(leukemia$wbc,"scaled:center")
sd_tdi <- attr(leukemia$tdi,"scaled:scale")
m_tdi <- attr(leukemia$tdi,"scaled:center")

# histograms of variables
dev.new()
par(mfrow=c(2,3))
hist(leukemia$time)
hist(leukemia$log_time)
hist(leukemia$age)
hist(leukemia$sex)
hist(leukemia$wbc)
hist(leukemia$tdi)

# indices of observations
set.seed(115)
ind <- sample(1:dim(leukemia)[1],300)	# select 300 observations out of the 1043 in order to be able to compute the exact GP in not too much time.
# ind <- 1:dim(leukemia)[1]		# select all the number of observations
N <- length(ind)

# indices of uncensored (obs) and censored (cens) observations
obs <- which(leukemia$cens[ind] == 1)
cens <- which(leukemia$cens[ind] == 0)
Nobs <- length(obs)
Ncens <- length(cens)

# indices for test observations
set.seed(115)
obs_test <- sample(obs, 0)
Ntest <- length(obs_test)

# indices for training observations
obs_train <- setdiff(obs, obs_test)
Ntrain <- length(obs_train)

# covariates
x1 <- leukemia$age[ind]
x2 <- leukemia$wbc[ind]
x3 <- leukemia$tdi[ind]
x4 <- leukemia$sex[ind]
X <- data.frame(x1, x2, x3, x4)

# indices of observations belonging to sex1 (male?) and to sex2 (female?) 
sex1 <- which(X$x4== 1)
Nsex1 <- length(sex1)
sex2 <- which(X$x4== -1)
Nsex2 <- length(sex2)

N == Nobs + Ncens

# response variable
y <- leukemia$log_time[ind]


### INPUTS VALUES TO CREATE SOME PLOTS
# inputs to evaluate the posterior for conditional plots
Nx1_grid <- 20 #length of these inputs
x1_grid <- seq(min(leukemia$age[ind]), max(leukemia$age[ind]), length.out=Nx1_grid) 
x2_grid <- seq(min(leukemia$wbc[ind]), max(leukemia$wbc[ind]), length.out=Nx1_grid) 
x3_grid <- seq(min(leukemia$tdi[ind]), max(leukemia$tdi[ind]), length.out=Nx1_grid) 

# for plotting y vs x1
X1 <- data.frame(x1=x1_grid, x2=rep(0, length(x1_grid)), x3=rep(0, length(x1_grid)), idx= "X1") 

# for plotting y vs x2
X2 <- data.frame(x1=rep(0, length(x1_grid)), x2=x2_grid, x3=rep(0, length(x1_grid)), idx= "X2")

# for plotting y vs x3
X3 <- data.frame(x1=rep(0, length(x1_grid)), x2=rep(0, length(x1_grid)), x3=x3_grid, idx= "X3")

# for plotting y vs x2 conditioned to x3=-1-m_tdi
X2_1 <- data.frame(x1=rep(0, length(x1_grid)), x2=x2_grid, x3=rep((-1-m_tdi)/sd_tdi, length(x1_grid)), idx= "X2_1")

# for plotting y vs x2 conditioned to x3=6-m_tdi
X2_2 <- data.frame(x1=rep(0, length(x1_grid)), x2=x2_grid, x3=rep((6-m_tdi)/sd_tdi, length(x1_grid)), idx= "X2_2")

# all these inputs toguether in a matrix
Xgrid <- rbind(X1,X2,X3,X2_1,X2_2)
Ngrid <- dim(Xgrid)[1]



########################
####  Hierarchical GP

standata_gp <- list()
standata_gp$obs <- obs
standata_gp$Nobs <- Nobs
standata_gp$obs_test <- obs_test
standata_gp$Ntest <- Ntest
standata_gp$obs_train <- obs_train
standata_gp$Ntrain <- Ntrain
standata_gp$cens <- cens
standata_gp$Ncens <- Ncens
standata_gp$D <- 3 			# dimensions
standata_gp$X <- X[,1:3]
standata_gp$Xgrid <- Xgrid
standata_gp$Ngrid <- Ngrid
standata_gp$y <- y
standata_gp$sex1 <- sex1
standata_gp$Nsex1 <- Nsex1
standata_gp$sex2 <- sex2
standata_gp$Nsex2 <- Nsex2


aj_gp_ml <- stan(file= ".../model_GP_mlevel.stan", data= standata_gp, iter= 300,  warmup= 200, chains= 1, thin= 1, algorithm= "NUTS")


summary(aj_gp_ml, pars = c("rho","alpha","sigma"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
summary(aj_gp_ml)$summary


# Storing results
gp_f <- list()
gp_f_grid_sex1 <- list()
gp_f_grid_sex2 <- list()

gp_f <- summary(aj_gp_ml, pars = c("f"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary

gp_f_grid_sex1 <- summary(aj_gp_ml, pars = c("f_predict_sex1"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary

gp_f_grid_sex2 <- summary(aj_gp_ml, pars = c("f_predict_sex2"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary


# Plots
dev.new()
par(mfrow=c(2,2))

hist(y)
hist(gp_f[,1])
plot(y, gp_f[1:(Nobs+Ncens),1], col=4, cex=0.6, xlab="y", ylab="gp_f"); abline(a=0, b=1, col="gray")

			
# indices for grid inputs
indX1 <- Xgrid$idx=="X1"
indX2 <- Xgrid$idx=="X2"
indX3 <- Xgrid$idx=="X3"
indX2_1 <- Xgrid$idx=="X2_1"
indX2_2 <- Xgrid$idx=="X2_2"


# Plots
dev.new()
par(mfrow=c(2,2))

matplot(x1_grid * sd_age + m_age, exp(gp_f_grid_sex1[indX1,c(1,4,6)] + gp_f_grid_sex2[indX1,c(1)] + m_time), log="y", type="l", lty=c(1,2,2), col=2, xlab="age", ylab="gp_f")
matplot(x1_grid * sd_age + m_age, exp(gp_f_grid_sex2[indX1,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=4, xlab="age", ylab="gp_f",add=TRUE)
legend("topright", legend=c("sex2", "sex1"), col=c(2,4), lty=1) 

matplot(x2_grid * sd_wbc + m_wbc, exp(gp_f_grid_sex1[indX2,c(1,4,6)] + gp_f_grid_sex2[indX2,c(1)] + m_time), log="y", type="l", lty=c(1,2,2), col=2, xlab="wbc", ylab="gp_f")
matplot(x2_grid * sd_wbc + m_wbc, exp(gp_f_grid_sex2[indX2,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=4, xlab="wbc", ylab="gp_f", add=TRUE)
legend("topright", legend=c("sex2", "sex1"), col=c(2,4), lty=1) 

matplot(x3_grid * sd_tdi + m_tdi, exp(gp_f_grid_sex1[indX3,c(1,4,6)] + gp_f_grid_sex2[indX3,c(1)] + m_time), log="y", type="l", lty=c(1,2,2), col=2, xlab="tdi", ylab="gp_f")
matplot(x3_grid * sd_tdi + m_tdi, exp(gp_f_grid_sex2[indX3,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=4, xlab="tdi", ylab="gp_f", add=TRUE)
legend("topright", legend=c("sex2", "sex1"), col=c(2,4), lty=1)

matplot(x3_grid * sd_tdi + m_tdi, exp(gp_f_grid_sex2[indX2_1,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=2, xlab="tdi", ylab="gp_f")
matplot(x3_grid * sd_tdi + m_tdi, exp(gp_f_grid_sex2[indX2_2,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=4, xlab="tdi", ylab="gp_f", add=TRUE)
legend("topright", legend=c("sex2, tdi=-1", "sex2, tdi=6"), col=c(2,4), lty=1) 	 


#######################
####  Hierarchical BF 

# The lengthscales values estimated in the exact GP model are around 4.00 for sex1 and 3.00 for sex2.

# The bounds of the input data are:
# max(abs(x1)) = 2.54
# max(abs(x2)) = 2.09
# max(abs(x3)) = 2.35

# So, it is a quite smooth latent function, with a lengthscale to half-data-range ratio (rho/S) around 1-1.5.

# Looking the graph (Graph_relation_M_lengthscale_L.png) of the relation between the lengthscale to half-data-range ratio (rho/S), the number of basis functions M, and the boundary condition L (L= c·S) (S= half-data-range). 

# We expect a low number of basis functions and a large factor c.

# We try the number of basis functions  M=c(5, 7, 10) and values for the factor c=c(3, 4, 5).

# The value that seems to have better results is c=3.

# A value of 2 or less for the factor c tends to differentiate from the GP solution.

# As we have 3 dimensions, more than 10 basis functions starts to be slow.


D <- 3
M <- c(5,7,10) 
c <- 3  #5  #4 

indices <- list()
for(j in 1:length(M)){
	indices[[j]] <- matrix(NA, M[j]^D, D)
	mm=0;
	for (m1 in 1:M[j]){
		for (m2 in 1:M[j]){
			for (m3 in 1:M[j]){
				mm = mm+1
				indices[[j]][mm,] = c(m1, m2, m3)
			}
		}
	}
}

standata_bf <- list()
for(j in 1:length(M)){
  	standata_bf[[j]] <- standata_gp
	standata_bf[[j]]$D <- D
	standata_bf[[j]]$M <- M[j]
	standata_bf[[j]]$M_nD <- M[j]^D
	standata_bf[[j]]$indices <- indices[[j]]
	standata_bf[[j]]$L <- c(c*max(abs(x1)), c*max(abs(x2)), c*max(abs(x3)))
	standata_bf[[j]]$X <- X[,1:3]
	standata_bf[[j]]$X1 <- X1[,1:3] 
	standata_bf[[j]]$X2 <- X2[,1:3]
	standata_bf[[j]]$X3 <- X3[,1:3]
	standata_bf[[j]]$X2_1 <- X2_1[,1:3]
	standata_bf[[j]]$X2_2 <- X2_2[,1:3]
	standata_bf[[j]]$Nx1_grid <- Nx1_grid
}


aj_bf_ml <- list()
for(j in 2:2){
	aj_bf_ml[[j]] <- stan(file= ".../model_BF_mlevel.stan", data= standata_bf[[j]], iter= 1000,  warmup= 500, chains= 1, thin= 1, algorithm= "NUTS")
}


summary(aj_bf_ml[[2]], pars = c("rho1","rho2","alpha","sigma","c0"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
summary(aj_bf_ml[[2]], pars = c("beta"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
summary(aj_bf_ml[[2]], pars = c("f"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary


# Storing results
bf_f <- list()
bf_f1 <- list()
bf_f1_sex1 <- list()
bf_f2 <- list()
bf_f2_sex1 <- list()
bf_f3 <- list()
bf_f3_sex1 <- list()

bf_f2_1 <- list()
bf_f2_1_sex1 <- list()
bf_f2_2 <- list()
bf_f2_2_sex1 <- list()

bf_resi <- list()
for(j in 2:2){
	bf_f[[j]] <- summary(aj_bf_ml[[j]], pars = c("f"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f1[[j]] <- summary(aj_bf_ml[[j]], pars = c("f1"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f1_sex1[[j]] <- summary(aj_bf_ml[[j]], pars = c("f1_sex1"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f2[[j]] <- summary(aj_bf_ml[[j]], pars = c("f2"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f2_sex1[[j]] <- summary(aj_bf_ml[[j]], pars = c("f2_sex1"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f3[[j]] <- summary(aj_bf_ml[[j]], pars = c("f3"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f3_sex1[[j]] <- summary(aj_bf_ml[[j]], pars = c("f3_sex1"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary

	bf_f2_1[[j]] <- summary(aj_bf_ml[[j]], pars = c("f2_1"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f2_1_sex1[[j]] <- summary(aj_bf_ml[[j]], pars = c("f2_1_sex1"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f2_2[[j]] <- summary(aj_bf_ml[[j]], pars = c("f2_2"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
	bf_f2_2_sex1[[j]] <- summary(aj_bf_ml[[j]], pars = c("f2_2_sex1"), probs = c(0.025, 0.5, 0.975), digits_summary = 4)$summary
}

# Plots
for(j in 2:2){
	dev.new()
	par(mfrow=c(2,2))

	hist(y)
	hist(bf_f[[j]][,1])
	plot(y, bf_f[[j]][,1], col=4, cex=0.6, xlab="log(y)", ylab="bf_f"); abline(a=0, b=1, col="gray")
}

# Plots
for(j in 2:2){
	dev.new()
	par(mfrow=c(2,2))
	
	matplot(x1_grid * sd_age + m_age, exp(bf_f1[[j]][,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=2, xlab="age", ylab="bf_f", ylim=c(20,2000))
	matplot(x1_grid * sd_age + m_age, exp(bf_f1_sex1[[j]][,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=4, xlab="age", ylab="bf_f", add=TRUE)
	legend("topright", legend=c("sex2", "sex1"), col=c(2,4), lty=1) 
	
	matplot(x2_grid * sd_wbc + m_wbc, exp(bf_f2[[j]][,c(1,4,6)] + attr(leukemia$log_time,"scaled:center")), log="y", type="l", lty=c(1,2,2), col=2, xlab="wbc", ylab="bf_f", ylim=c(50,350))
	matplot(x2_grid * sd_wbc + m_wbc, exp(bf_f2_sex1[[j]][,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=4, xlab="wbc", ylab="bf_f", add=TRUE)
	legend("topright", legend=c("sex2", "sex1"), col=c(2,4), lty=1) 
	
	matplot(x3_grid * sd_tdi + m_tdi, exp(bf_f3[[j]][,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=2, xlab="tdi", ylab="bf_f", ylim=c(100,700))
	matplot(x3_grid * sd_tdi + m_tdi, exp(bf_f3_sex1[[j]][,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=4, xlab="tdi", ylab="bf_f", add=TRUE)
	legend("topright", legend=c("sex2", "sex1"), col=c(2,4), lty=1) 
	
	matplot(x2_grid * sd_wbc + m_wbc, exp(bf_f2_1[[j]][,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=2, xlab="wbc", ylab="bf_f", ylim=c(30,500))
	matplot(x2_grid * sd_wbc + m_wbc, exp(bf_f2_2[[j]][,c(1,4,6)] + m_time), log="y", type="l", lty=c(1,2,2), col=4, xlab="wbc", ylab="bf_f", add=TRUE)
	legend("topright", legend=c("sex2, tdi=-1", "sex2, tdi=6"), col=c(2,4), lty=1) 
}


























