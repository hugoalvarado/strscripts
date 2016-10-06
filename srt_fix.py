import os
import re

'''
SRT Subtitles consist of four parts, all in text

1. A number indicating which subtitle it is in the sequence.
2. The time that the subtitle should appear on the screen, and then disappear.
3. The subtitle itself.
4. A blank line indicating the start of a new subtitle.

This script will fix subtitles missing the sequence number such as:

1
00:00:00.00 --> 00:00:05.00

00:00:32.00 --> 00:00:35.00
What a really bad day

00:01:33.00 --> 00:01:37.00
What is it now this early?

4
00:01:38.00 --> 00:01:42.00
(PHONE RINGS)
'''



source_srt = open('input.srt')
dest_srt =  open('output.srt', 'w')

srt_lines = source_srt.readlines()

subtitle_buffer = ""
srt_count = 0
section_count = 0 

numRegex = re.compile(r'^\d+$')

for line in srt_lines:
    
    #skip blank lines
    if len(line) == 0:
        continue

    #skip index/sequence rows, we will rebuild this value
    if numRegex.match(line.strip()):
        continue
        
    #we found a time section
    if '-->' in line:
        section_count += 1
    
    #we have completed reading a whole subtitle section, write it out
    if section_count == 2:
        srt_count += 1
        dest_srt.write(str(srt_count)+'\n')        
        dest_srt.write(subtitle_buffer)        
              
        #reset counter and buffer
        subtitle_buffer = ""
        section_count = 1
    
    
    #add the line to our buffer
    subtitle_buffer += line   


    if srt_count == 1:
        break 
    

#write the last bit
dest_srt.write(str(srt_count+1)+'\n')        
dest_srt.write(subtitle_buffer)

source_srt.close()
dest_srt.close()        