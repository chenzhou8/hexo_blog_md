title: CSAPP-LAB4-perflab-handout优化方案
date: 2015-11-30 19:37
categories: 操作系统
tags: 操作系统

---


### 实验环境：
Linux 3.13.11-ckt27-终端

---

### README：

```
#####################################################################
# CS:APP Performance Lab
#
# Student's Source Files
#
# Copyright (c) 2002, R. Bryant and D. O'Hallaron, All rights reserved.
# May not be used, modified, or copied without permission.
#
######################################################################

This directory contains the files you will need for the CS:APP
Performance Lab.

kernels.c
	This is the file you will be modifying and handing in. 

#########################################
# You shouldn't modify any of these files
#########################################
driver.c
	This is the driver that tests the performance of all 
	of the versions of the rotate and smooth kernels 
	in your kernels.c file.

config.h
	This is a site-specific configuration file that was created by 
	your instructor	for your system.

defs.h
	Various definitions needed by kernels.c and driver.c

clock.{c,h}
fcyc.{c,h}
	These contain timing routines that measure the performance of your
	code with our k-best measurement scheme using IA32 cycle counters.

Makefile:
	This is the makefile that builds the driver program.
```

优化的三个版本：rotate1、rotate2、rotate3与smooth1、smooth2、smooth3如下：


<!--more-->

### kernels.c:
```
     /********************************************************
     * Kernels to be optimized for the CS:APP Performance Lab
     ********************************************************/
    #include <stdio.h>
    #include <stdlib.h>
    #include "defs.h"

    /* 
     * Please fill in the following team struct 
     */
    team_t team = {
        "longyun.club",             /* Team name */
        "longyun.club",             /* First member full name */
        "lxl@longyun.club",         /* First member email address */
        "longyun.club",             /* Second member full name (leave blank if none) */
        "lxl@longyun.club"          /* Second member email addr (leave blank if none) */
    };

    /***************
      * ROTATE KERNEL
    ***************/

    /******************************************************
     * Your different versions of the rotate kernel go here
     ******************************************************/

    /* 
     * naive_rotate - The naive baseline version of rotate 
     */
    char naive_rotate_descr[] = "naive_rotate: Naive baseline implementation";
    void naive_rotate(int dim, pixel *src, pixel *dst) 
    {
        int i, j;
        for (i = 0; i < dim; i++)
	    for (j = 0; j < dim; j++)
	    dst[RIDX(dim-1-j, i, dim)] = src[RIDX(i, j, dim)];
     }

    /* 
     * rotate - Your current working version of rotate
     * IMPORTANT: This is the version you will be graded on
     */
    //1111111
    char rotate_descr[] = "rotate1: ...";
    void rotate(int dim, pixel *src, pixel*dst)
    {
        int i,j,i1,j1;
        for(i1=0;i1<dim;i1+=4)
            for(j1=0;j1<dim;j1+=4)
                for(i=i1;i<i1+4;i++)
                    for(j=j1;j<j1+4;j++)
                        dst[RIDX(dim-1-j,i,dim)]=src[RIDX(i,j,dim)];
        for(i1=0;i1<dim;i1+=32)
            for(j1=0;j1<dim;j1+=32)
                for(i=j1;i<i1+32;i+=1)
                    for(j=j1;j<j1+32;j+=1)
                        dst[RIDX(dim-1-j,i,dim)]=  src[RIDX(i,j,dim)];
    }

    //222222
    char rotate_descr2[] = "rotate2: ...";
    void rotate2(int dim, pixel *src, pixel*dst)
    {
        int i;
        int j;
        int tmp1=dim*dim;
        int tmp2=dim *31;
        int tmp3=tmp1-dim;
        int tmp4=tmp1+32;
        int tmp5=dim+31;
        dst+=tmp3; 
        for(i=0; i< dim; i+=32) 
        {         
            for(j=0;j<dim;j++)
            {       
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;  
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;
                dst++; src+=dim;
                *dst=*src;        
                src++;
                src-=tmp2;
                dst-=tmp5;
            }
            src+=tmp2;
            dst+=tmp4;
        }            
    } 

    //333333
    #define COPY(d,s) *(d)=*(s)
    char rotate_descr3[] = "rotate3: ...";
    void rotate3( int dim,pixel *src,pixel *dst)
    {
        int i,j;
        for(i=0;i<dim;i+=32)
        {
            for(j=dim-1;j>=0;j-=1)
            {       
                pixel*dptr=dst+RIDX(dim-1-j,i,dim);
                pixel*sptr=src+RIDX(i,j,dim);
                COPY(dptr,sptr); sptr+=dim;
                COPY(dptr+1,sptr); sptr+=dim;
                COPY(dptr+2,sptr); sptr+=dim;
                COPY(dptr+3,sptr); sptr+=dim;
                COPY(dptr+4,sptr); sptr+=dim;
                COPY(dptr+5,sptr); sptr+=dim;
                COPY(dptr+6,sptr); sptr+=dim;
                COPY(dptr+7,sptr); sptr+=dim;
                COPY(dptr+8,sptr); sptr+=dim;
                COPY(dptr+9,sptr); sptr+=dim;
                COPY(dptr+10,sptr); sptr+=dim;
                COPY(dptr+11,sptr); sptr+=dim;
                COPY(dptr+12,sptr); sptr+=dim;
                COPY(dptr+13,sptr); sptr+=dim;
                COPY(dptr+14,sptr); sptr+=dim;
                COPY(dptr+15,sptr); sptr+=dim;
                COPY(dptr+16,sptr); sptr+=dim;
                COPY(dptr+17,sptr); sptr+=dim;
                COPY(dptr+18,sptr); sptr+=dim;
                COPY(dptr+19,sptr); sptr+=dim;
                COPY(dptr+20,sptr); sptr+=dim;
                COPY(dptr+21,sptr); sptr+=dim;
                COPY(dptr+22,sptr); sptr+=dim;
                COPY(dptr+23,sptr); sptr+=dim;
                COPY(dptr+24,sptr); sptr+=dim;
                COPY(dptr+25,sptr); sptr+=dim;
                COPY(dptr+26,sptr); sptr+=dim;
                COPY(dptr+27,sptr); sptr+=dim;
                COPY(dptr+28,sptr); sptr+=dim;
                COPY(dptr+29,sptr); sptr+=dim;
                COPY(dptr+30,sptr); sptr+=dim;
                COPY(dptr+31,sptr);
            }
        }
    }

    /*********************************************************************
     * register_rotate_functions - Register all of your different versions
     *     of the rotate kernel with the driver by calling the
     *     add_rotate_function() for each test function. When you run the
     *     driver program, it will test and report the performance of each
     *     registered test function. 
     *********************************************************************/

    void register_rotate_functions() 
    {
        /* ... Register additional test functions here */
        add_rotate_function(&naive_rotate, naive_rotate_descr);
        add_rotate_function(&rotate, rotate_descr);
        add_rotate_function(&rotate2, rotate_descr2);
        add_rotate_function(&rotate3, rotate_descr3);   
    }

    /***************
     * SMOOTH KERNEL
     **************/

    /***************************************************************
     * Various typedefs and helper functions for the smooth function
     * You may modify these any way you like.
     **************************************************************/

    /* A struct used to compute averaged pixel value */
    typedef struct {
        int red;
        int green;
        int blue;
        int num;
    } pixel_sum;

    /* Compute min and max of two integers, respectively */
    static int min(int a, int b) { return (a < b ? a : b); }
    static int max(int a, int b) { return (a > b ? a : b); }

    /* 
     * initialize_pixel_sum - Initializes all fields of sum to 0 
     */
    static void initialize_pixel_sum(pixel_sum *sum) 
    {
        sum->red = sum->green = sum->blue = 0;
        sum->num = 0;
        return;
    }

    /* 
    * accumulate_sum - Accumulates field values of p in corresponding 
    * fields of sum 
    */
    static void accumulate_sum(pixel_sum *sum, pixel p) 
    {
        sum->red += (int) p.red;
        sum->green += (int) p.green;
        sum->blue += (int) p.blue;
        sum->num++;
        return;
    }

    /* 
     * assign_sum_to_pixel - Computes averaged pixel value in current_pixel 
     */
    static void assign_sum_to_pixel(pixel *current_pixel, pixel_sum sum) 
    {
        current_pixel->red = (unsigned short) (sum.red/sum.num);
        current_pixel->green = (unsigned short) (sum.green/sum.num);
        current_pixel->blue = (unsigned short) (sum.blue/sum.num);
        return;
    }

    /* 
     * avg - Returns averaged pixel value at (i,j) 
     */
    static pixel avg(int dim, int i, int j, pixel *src) 
    {
        int ii, jj;
        pixel_sum sum;
        pixel current_pixel;
        initialize_pixel_sum(&sum);
        for(ii = max(i-1, 0); ii <= min(i+1, dim-1); ii++) 
	        for(jj = max(j-1, 0); jj <= min(j+1, dim-1); jj++) 
	            accumulate_sum(&sum, src[RIDX(ii, jj, dim)]);
        assign_sum_to_pixel(&current_pixel, sum);
        return current_pixel;
    }

    /******************************************************
     * Your different versions of the smooth kernel go here
     ******************************************************/

    /*
     * naive_smooth - The naive baseline version of smooth 
    */
    char naive_smooth_descr[] = "naive_smooth: Naive baseline implementation";
    void naive_smooth(int dim, pixel *src, pixel *dst) 
    {
        int i, j;
        for (i = 0; i < dim; i++)
	        for (j = 0; j < dim; j++)
	            dst[RIDX(i, j, dim)] = avg(dim, i, j, src);
    }

    /*
     * smooth - Your current working version of smooth. 
     * IMPORTANT: This is the version you will be graded on
     */

    //111111
    #define fastmin(a,b)  (a < b ? a : b)
    #define fastmax(a, b) (a > b ? a : b)
    char smooth_descr[] = "smooth1: ...";
    void smooth(int dim, pixel *src, pixel *dst)
    {
        int i, j;
        for (i = 0; i < dim; i++)
        {
            for (j = 0; j < dim; j++)
            {
                int ii, jj;
                pixel_sum sum;
                pixel current_pixel;
                sum.red = sum.green = sum.blue = 0;
                sum.num = 0;
                for(ii= fastmax(i-1, 0); ii <= fastmin(i+1, dim-1); ii++)
                {
                    for(jj = fastmax(j-1, 0); jj <=fastmin(j+1, dim-1); jj++)
                    {
                        pixel p=src[RIDX(ii, jj, dim)];
                        sum.red += (int) p.red;
                        sum.green+= (int) p.green;
                        sum.blue+= (int) p.blue;
                        sum.num++;
                    }
                    current_pixel.red = (unsigned short)(sum.red/sum.num);
                    current_pixel.green = (unsigned short)(sum.green/sum.num);
                    current_pixel.blue= (unsigned short) (sum.blue/sum.num);
                    dst[RIDX(i, j, dim)] = current_pixel;
                }
            }
	    }
    }

    //222222
    char smooth_descr2[] = "smooth2: ...";
    void smooth2(int dim, pixel *src, pixel *dst)
    {
        pixel_sum rowsum[530][530];
        int i, j, snum;
        for(i=0;i<dim; i++)
        {
            rowsum[i][0].red = (src[RIDX(i, 0, dim)].red+src[RIDX(i, 1, dim)].red);
            rowsum[i][0].blue = (src[RIDX(i, 0, dim)].blue+src[RIDX(i, 1,dim)].blue);
            rowsum[i][0].green = (src[RIDX(i, 0, dim)].green+src[RIDX(i, 1,dim)].green);
            rowsum[i][0].num = 2;
            for(j=1;j<dim-1; j++)
            {
                rowsum[i][j].red = (src[RIDX(i, j-1, dim)].red+src[RIDX(i, j,dim)].red+src[RIDX(i, j+1, dim)].red);
                rowsum[i][j].blue = (src[RIDX(i, j-1, dim)].blue+src[RIDX(i, j,dim)].blue+src[RIDX(i, j+1, dim)].blue);
                rowsum[i][j].green = (src[RIDX(i, j-1, dim)].green+src[RIDX(i, j,dim)].green+src[RIDX(i, j+1, dim)].green);
                rowsum[i][j].num = 3;
            }
            rowsum[i][dim-1].red = (src[RIDX(i, dim-2, dim)].red+src[RIDX(i, dim-1,dim)].red);
            rowsum[i][dim-1].blue = (src[RIDX(i, dim-2, dim)].blue+src[RIDX(i,dim-1, dim)].blue);
            rowsum[i][dim-1].green = (src[RIDX(i, dim-2, dim)].green+src[RIDX(i,dim-1, dim)].green);
            rowsum[i][dim-1].num = 2;
        }
        for(j=0;j<dim; j++)
        {
            snum = rowsum[0][j].num+rowsum[1][j].num;
            dst[RIDX(0,j, dim)].red = (unsigned short)((rowsum[0][j].red+rowsum[1][j].red)/snum);
            dst[RIDX(0,j, dim)].blue = (unsigned short)((rowsum[0][j].blue+rowsum[1][j].blue)/snum);
            dst[RIDX(0,j, dim)].green = (unsigned short)((rowsum[0][j].green+rowsum[1][j].green)/snum);
            for(i=1;i<dim-1; i++)
            {
                snum =rowsum[i-1][j].num+rowsum[i][j].num+rowsum[i+1][j].num;
                dst[RIDX(i, j, dim)].red = (unsigned short)((rowsum[i-1][j].red+rowsum[i][j].red+rowsum[i+1][j].red)/snum);
                dst[RIDX(i, j, dim)].blue = (unsigned short)((rowsum[i-1][j].blue+rowsum[i][j].blue+rowsum[i+1][j].blue)/snum);
                dst[RIDX(i, j, dim)].green = (unsigned short)((rowsum[i-1][j].green+rowsum[i][j].green+rowsum[i+1][j].green)/snum);
            }
            snum =rowsum[dim-1][j].num+rowsum[dim-2][j].num;
            dst[RIDX(dim-1, j, dim)].red = (unsigned short)((rowsum[dim-2][j].red+rowsum[dim-1][j].red)/snum);
            dst[RIDX(dim-1, j, dim)].blue = (unsigned short)((rowsum[dim-2][j].blue+rowsum[dim-1][j].blue)/snum);
            dst[RIDX(dim-1, j, dim)].green = (unsigned short)((rowsum[dim-2][j].green+rowsum[dim-1][j].green)/snum);
        }
    }

    //333333
    char smooth_descr3[] = "smooth3: ...";
    void smooth3(int dim, pixel *src, pixel *dst)
    {
        int i, j, rij;
        int rindex = dim;
        // Corner cases
        dst[0].red = (src[0].red+src[1].red+src[dim].red+src[dim+1].red)>>2;
        dst[0].blue = (src[0].blue+src[1].blue+src[dim].blue+src[dim+1].blue)>>2;
        dst[0].green = (src[0].green+src[1].green+src[dim].green+src[dim+1].green)>>2;
        dst[dim-1].red = (src[dim-1].red+src[dim-2].red+src[dim*2-1].red+src[dim*2-2].red)>>2;
        dst[dim-1].blue = (src[dim-1].blue+src[dim-2].blue+src[dim*2-1].blue+src[dim*2-2].blue)>>2;
        dst[dim-1].green = (src[dim-1].green+src[dim-2].green+src[dim*2-1].green+src[dim*2-2].green)>>2;
    
        dst[dim*(dim-1)].red = (src[dim*(dim-1)].red+src[dim*(dim-1)+1].red+src[dim*(dim-2)].red+src[dim*(dim-2)+1].red)>>2;
        dst[dim*(dim-1)].blue = (src[dim*(dim-1)].blue+src[dim*(dim-1)+1].blue+src[dim*(dim-2)].blue+src[dim*(dim-2)+1].blue)>>2;
        dst[dim*(dim-1)].green = (src[dim*(dim-1)].green+src[dim*(dim-1)+1].green+src[dim*(dim-2)].green+src[dim*(dim-2)+1].green)>>2;
    
        dst[dim*dim-1].red = (src[dim*dim-1].red+src[dim*dim-2].red+src[dim*(dim-1)-1].red+src[dim*(dim-1)-2].red)>>2;
        dst[dim*dim-1].blue = (src[dim*dim-1].blue+src[dim*dim-2].blue+src[dim*(dim-1)-1].blue+src[dim*(dim-1)-2].blue)>>2;
        dst[dim*dim-1].green = (src[dim*dim-1].green+src[dim*dim-2].green+src[dim*(dim-1)-1].green+src[dim*(dim-1)-2].green)>>2;
        for (j = 1; j < dim-1; j++)
        {
            dst[j].red = (src[j].red+src[j-1].red+src[j+1].red+src[j+dim].red+src[j+1+dim].red+src[j-1+dim].red)/6;
            dst[j].green = (src[j].green+src[j-1].green+src[j+1].green+src[j+dim].green+src[j+1+dim].green+src[j-1+dim].green)/6;
            dst[j].blue = (src[j].blue+src[j-1].blue+src[j+1].blue+src[j+dim].blue+src[j+1+dim].blue+src[j-1+dim].blue)/6;
        }
        for (j = dim*(dim-1)+1; j < dim*dim-1; j++)
        {
            dst[j].red = (src[j].red+src[j-1].red+src[j+1].red+src[j-dim].red+src[j+1-dim].red+src[j-1-dim].red)/6;
            dst[j].green = (src[j].green+src[j-1].green+src[j+1].green+src[j-dim].green+src[j+1-dim].green+src[j-1-dim].green)/6;
            dst[j].blue = (src[j].blue+src[j-1].blue+src[j+1].blue+src[j-dim].blue+src[j+1-dim].blue+src[j-1-dim].blue)/6;
        }
        for (j = dim; j < dim*(dim-1); j+=dim)
        {
            dst[j].red = (src[j].red+src[j-dim].red+src[j+1].red+src[j+dim].red+src[j+1+dim].red+src[j-dim+1].red)/6;
            dst[j].green = (src[j].green+src[j-dim].green+src[j+1].green+src[j+dim].green+src[j+1+dim].green+src[j-dim+1].green)/6;
            dst[j].blue = (src[j].blue+src[j-dim].blue+src[j+1].blue+src[j+dim].blue+src[j+1+dim].blue+src[j-dim+1].blue)/6;
        }
        for (j = dim+dim-1; j < dim*dim-1; j+=dim)
        {
            dst[j].red = (src[j].red+src[j-1].red+src[j-dim].red+src[j+dim].red+src[j-dim-1].red+src[j-1+dim].red)/6;
            dst[j].green = (src[j].green+src[j-1].green+src[j-dim].green+src[j+dim].green+src[j-dim-1].green+src[j-1+dim].green)/6;
            dst[j].blue = (src[j].blue+src[j-1].blue+src[j-dim].blue+src[j+dim].blue+src[j-dim-1].blue+src[j-1+dim].blue)/6;
        }
        for (i = 1; i < dim-1; i++)
        {
            for (j = 1; j < dim-1; j++)
            {
                rij = rindex+j;
                dst[rij].red = (src[rij].red+src[rij-1].red+src[rij+1].red+src[rij-dim].red+src[rij-dim-1].red+src[rij-dim+1].red+src[rij+dim].red+src[rij+dim+1].red+src[rij+dim-1].red)/9;
                dst[rij].green = (src[rij].green+src[rij-1].green+src[rij+1].green+src[rij-dim].green+src[rij-dim-1].green+src[rij-dim+1].green+src[rij+dim].green+src[rij+dim+1].green+src[rij+dim-1].green)/9;
                dst[rij].blue = (src[rij].blue+src[rij-1].blue+src[rij+1].blue+src[rij-dim].blue+src[rij-dim-1].blue+src[rij-dim+1].blue+src[rij+dim].blue+src[rij+dim+1].blue+src[rij+dim-1].blue)/9;
            }
            rindex += dim;
        }
    }

    /********************************************************************* 
     * register_smooth_functions - Register all of your different versions
     *     of the smooth kernel with the driver by calling the
     *     add_smooth_function() for each test function.  When you run the
     *     driver program, it will test and report the performance of each
     *     registered test function. 
     *********************************************************************/
    void register_smooth_functions()
    {
        /* ... Register additional test functions here */
        add_smooth_function(&smooth, smooth_descr);
        add_smooth_function(&smooth2, smooth_descr2);
        add_smooth_function(&smooth3, smooth_descr3);
        add_smooth_function(&naive_smooth, naive_smooth_descr);
    }

```

通过：

```
make clean
make all
```

两条命令，生成driver可执行文件

通过：

```
./driver
```

得到以下结果：

```

➜  perflab-handout  ./driver 
Teamname: longyun.club
Member 1: longyun.club
Email 1: lxl@longyun.club
Member 2: longyun.club
Email 2: lxl@longyun.club

Rotate: Version = naive_rotate: Naive baseline implementation:
Dim		64	128	256	512	1024	Mean
Your CPEs	3.5	4.7	7.6	12.6	24.9
Baseline CPEs	14.7	40.1	46.4	65.9	94.5
Speedup		4.2	8.6	6.1	5.2	3.8	5.4

Rotate: Version = rotate1: ...:
Dim		64	128	256	512	1024	Mean
Your CPEs	7.4	8.8	13.1	29.6	87.7
Baseline CPEs	14.7	40.1	46.4	65.9	94.5
Speedup		2.0	4.6	3.5	2.2	1.1	2.4

Rotate: Version = rotate2: ...:
Dim		64	128	256	512	1024	Mean
Your CPEs	2.8	2.8	2.7	4.1	5.4
Baseline CPEs	14.7	40.1	46.4	65.9	94.5
Speedup		5.2	14.1	17.2	16.1	17.6	12.9

Rotate: Version = rotate3: ...:
Dim		64	128	256	512	1024	Mean
Your CPEs	2.9	3.0	3.0	4.9	6.1
Baseline CPEs	14.7	40.1	46.4	65.9	94.5
Speedup		5.0	13.5	15.2	13.3	15.6	11.6

Smooth: Version = smooth1: ...:
Dim		32	64	128	256	512	Mean
Your CPEs	124.5	125.5	125.9	126.2	127.1
Baseline CPEs	695.0	698.0	702.0	717.0	722.0
Speedup		5.6	5.6	5.6	5.7	5.7	5.6

Smooth: Version = smooth2: ...:
Dim		32	64	128	256	512	Mean
Your CPEs	48.6	50.8	51.7	55.1	60.3
Baseline CPEs	695.0	698.0	702.0	717.0	722.0
Speedup		14.3	13.7	13.6	13.0	12.0	13.3

Smooth: Version = smooth3: ...:
Dim		32	64	128	256	512	Mean
Your CPEs	22.0	25.3	25.5	25.9	26.3
Baseline CPEs	695.0	698.0	702.0	717.0	722.0
Speedup		31.5	27.6	27.5	27.7	27.5	28.3

Smooth: Version = naive_smooth: Naive baseline implementation:
Dim		32	64	128	256	512	Mean
Your CPEs	76.0	76.6	76.6	78.3	78.7
Baseline CPEs	695.0	698.0	702.0	717.0	722.0
Speedup		9.1	9.1	9.2	9.2	9.2	9.1

Summary of Your Best Scores:
  Rotate: 12.9 (rotate2: ...)
  Smooth: 28.3 (smooth3: ...)

```
