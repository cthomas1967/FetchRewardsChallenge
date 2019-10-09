Once we have converted a document into a single column of words and diffed the two documents, there are five cases to consider.

To illustrate these, it's useful to consider a source document of just one word in length.

1) The word is left unchanged.  

   The score is 1.0.

2) One word was removed from the source document and not replaced by anything.

   The score is 0.0.

3) One word was removed from the source document and replaced by exactly one word.

   The score is 0.0.

4) One word was removed from the source document and replaced by more than one word.
   
   Example: Source document has 1 word.  We remove one, but add 5 new words. 
   The score is 0.0.

5) One or more words were added to the source document without removing any words.

  Example: Source document has one word.  We add four new words.  
  The new score is 1/5 or 0.2.

Proposed algorithm: We score each line, then take the average of the lines.


