import matplotlib.pyplot as plt 
import numpy as np
voc=list()
ozone=list()
def plot_voc(voc,site_number):
	l2=list()
	for i in range(len(voc)):
				l2.append(int(i*10))
	i=1
	plt.plot(l2,voc,'-o')
	plt.xlim(0,200)
	plt.xticks(np.arange(0,100,10))
	plt.title("VOC Graph for site %d, MEAN= %d"%(site_number,np.mean(voc)))
	plt.xlabel("Time in Seconds")
	plt.ylabel("Voc in ppb")
	


def plot_ozone(ozone,site_number):
	l2=list()
	for i in range(len(ozone)):
				l2.append(int(i*45))
	i=1
	plt.plot(l2,ozone,'-o')
	plt.xlim(0,450)
	plt.xticks(np.arange(0,450,45))
	plt.title("OZONE Graph for site %d, MEAN=%d"%(site_number, np.mean(ozone)))
	plt.xlabel("Time in Seconds")
	plt.ylabel("Ozone in ppb")

def main():
	for j in range(6):
		voc=list()
		print('________________________________________')
		print('Site number: %d'%j)
		print('________________________________________')
		voc1=str(raw_input("Enter values for VOC:"))
		voc1=voc1.split(',')
		for ele in voc1:
			voc.append(int(ele))
		#ozone=list()
		#ozone1=str(raw_input("Enter values for Ozone:"))
		#ozone1=ozone1.split(",")
		#for ele in ozone1:
	    #	ozone.append(int(ele))
		plot_voc(voc,j+1)
		plt.show()
		i=str(raw_input("Do you want to continue (Y/n)"))
		#plot_ozone(ozone,j)
		#plt.show()

		if i == 'n' or i=='N':
			break
		#plot_ozone(ozone,j)


if __name__=='__main__':
	main()