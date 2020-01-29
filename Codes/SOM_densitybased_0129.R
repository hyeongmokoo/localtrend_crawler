rm(list=ls(all=TRUE)) 
library(rgdal)
library(kohonen)
library(dummies)
library(foreign)
library(RColorBrewer)

setwd("C:/Google Drive/Projects/2020/DataLab_SOM/Codes/Data") 

sample.shp <- readOGR(dsn=getwd(), layer="TL_SCCO_EMD_att")
sample.df <- as.data.frame(sample.shp)

data_train <- sample.df[,seq(62, 539, by = 53)]/sample.df[,540]

data_train_matrix <- as.matrix(scale(data_train))
names(data_train_matrix) <- names(data_train)

som_grid <- somgrid(xdim = 6, ydim=6, topo="hexagonal")

som_model <- som(data_train_matrix, grid=som_grid, rlen=1000, alpha=c(0.05,0.01), mode = "online", keep.data = TRUE)

##Developed from https://www.r-bloggers.com/self-organising-maps-for-customer-segmentation-using-r/

source('coolBlueHotRed.R')
plot(som_model, type = "changes")
#counts within nodes
plot(som_model, type = "counts", main="Node Counts", palette.name=coolBlueHotRed, shape = "straight")
#map quality
plot(som_model, type = "quality", main="Node Quality/Distance", palette.name=terrain.colors, shape = "straight")
#neighbour distances
plot(som_model, type="dist.neighbours", main = "SOM neighbour distances", palette.name=grey.colors)
#code spread
plot(som_model, type = "codes")

# Plot the heatmap for a variable at scaled / normalised values
for(i in 1:10){
  varnm <- names(som_model$data[[1]])[i]
  tif.path <- paste(varnm, ".tif", sep = "")
  tiff(tif.path, width = 8, height = 6, units = 'in', compression = "lzw", res = 300)
    plot(som_model, type = "property", property = som_model$codes[[1]][,i], main=varnm, palette.name=coolBlueHotRed)
  dev.off()
}


# ------------------ Clustering SOM results -------------------

# show the WCSS metric for kmeans for different clustering sizes.
# Can be used as a "rough" indicator of the ideal number of clusters
somres <- som_model$codes[[1]]
wss <- (nrow(somres)-1)*sum(apply(somres,2,var))
for (i in 2:15) 
  wss[i] <- sum(kmeans(somres, centers=i)$withinss)
par(mar=c(5.1,4.1,4.1,2.1))
plot(1:15, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares", main="Within cluster sum of squares (WCSS)")

# Form clusters on grid
## use hierarchical clustering to cluster the codebook vectors
n.clu <- 7
som_cluster <- cutree(hclust(dist(somres)), n.clu)

# Show the map with different colours for every cluster						  

bgcolors <- brewer.pal(n.clu, 'Set1')
plot(som_model, type="mapping", bgcol = bgcolors[as.integer(som_cluster)],  shape = "straight", main = "Clusters")
add.cluster.boundaries(som_model, som_cluster)

#show the same plot with the codes instead of just colours
plot(som_model, type="codes", bgcol = bgcolors[as.integer(som_cluster)], shape = "straight", main = "Clusters")
add.cluster.boundaries(som_model, som_cluster)

# -------------------- MAPPING OF SMALL AREAS (GEO) --------------------------
# Plot the map of ireland, coloured by the clusters the map to show locations.
cluster_details <- data.frame(id=sample.df$EMD_CD, cluster=som_cluster[som_model$unit.classif])
write.dbf(cluster_details, "someres_7_0129.dbf") ##For using in ArcMap.

##This is a map sample in R
sample.df$id <- sample.df$EMD_CD
mappoints <- fortify(sample.shp, region="EMD_CD")
mappoints <- merge(mappoints, sample.df, by="id")
mappoints <- merge(mappoints, cluster_details, by="id")

# Finally map the areas and colour by cluster
tiff(tif.path, width = 8, height = 6, units = 'in', compression = "lzw", res = 300)
ggplot(mappoints)+
  aes(long, lat, group=group, fill=factor(cluster))+
  geom_polygon()  + coord_equal() +
  scale_fill_manual(values = bgcolors) + geom_path(colour="white", alpha=0.4, size=0.1) 

dev.off()
