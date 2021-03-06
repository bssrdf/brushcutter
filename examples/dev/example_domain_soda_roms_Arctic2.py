from brushcutter import *

sodafile = '../data/soda3.3.1_5dy_ocean_reg_1980_09_29.nc'
romsgrd = '/Users/raphael/STORAGE/ROMS/GRIDS/grid_Arctic_2.nc'

# ---------- define segments on MOM grid -----------------------
domain = obc_segment('domain', romsgrd,istart=0,iend=689,jstart=0,  jend=1089,target_model='ROMS')

# ---------- define variables on each segment ------------------
temp_domain = obc_variable(domain,'temp',geometry='surface',obctype='radiation',debug=False)
salt_domain = obc_variable(domain,'salt',geometry='surface',obctype='radiation',debug=False)
ssh_domain  = obc_variable(domain,'ssh' ,geometry='line'   ,obctype='flather',debug=False)
vel_domain  = obc_vectvariable(domain,'u','v',geometry='surface',obctype='radiation',debug=False)

# ---------- interpolate T/S from WOA monthly file, frame = 0 (jan) and using locstream (x2 speedup)
interp_t2s = temp_domain.interpolate_from(sodafile,'temp',frame=0,depthname='st_ocean',coord_names=['xt_ocean','yt_ocean'],\
method='bilinear',drown='ncl',autocrop=False)
salt_domain.interpolate_from(sodafile,'salt',frame=0,depthname='st_ocean',coord_names=['xt_ocean','yt_ocean'],\
method='bilinear',drown='ncl',autocrop=False,interpolator=interp_t2s)
ssh_domain.interpolate_from(sodafile ,'ssh' ,frame=0,depthname='st_ocean',coord_names=['xt_ocean','yt_ocean'],\
method='bilinear',drown='ncl',autocrop=False,interpolator=interp_t2s)
# we can't reuse the previous interpolator because the source grid changes
interp_u2s, interp_v2s = vel_domain.interpolate_from(sodafile,'u','v',frame=0,depthname='st_ocean',\
coord_names_u=['xu_ocean','yu_ocean'],coord_names_v=['xu_ocean','yu_ocean'],\
method='bilinear',drown='ncl',autocrop=False)

# ---------- list segments and variables to be written -------
list_segments = [domain]

# ---------- write to two files ------------------------------
list_variables = [temp_domain,salt_domain,ssh_domain] 
list_vectvariables = []
time = temp_domain.timesrc

#lib_ioncdf.write_obc_file(list_segments,list_variables,list_vectvariables,time,output='soda3.3.1_5dy_ocean_reg_1980_09_29_domain_Arctic2_T.nc')

list_variables = [] 
list_vectvariables = [vel_domain]
time = vel_domain.timesrc

#lib_ioncdf.write_obc_file(list_segments,list_variables,list_vectvariables,time,output='soda3.3.1_5dy_ocean_reg_1980_09_29_domain_Arctic2_UV.nc')

# ---------- write to single file ----------------------------
list_variables = [temp_domain,salt_domain,ssh_domain] 
list_vectvariables = [vel_domain]
time = temp_domain.timesrc
lib_ioncdf.write_obc_file(list_segments,list_variables,list_vectvariables,time,output='soda3.3.1_5dy_ocean_reg_1980_09_29_domain_Arctic2.nc')
