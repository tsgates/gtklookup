(eval-when-compile
  (require 'browse-url)
  (require 'simple)
  (require 'cl)
  (require 'ido)
  (require 'anything))

;;=================================================================
;; user options
;;=================================================================

(defvar gtklookup-db-file "gtklookup.db" "gtklookup database file")
(defvar gtklookup-program "gtklookup.py" "gtklookup execution file")

(defvar gtklookup-all   nil)
(defvar gtklookup-cache nil)

;;=================================================================
;; execute gtklookup
;;=================================================================

(defun gtklookup-exec-get-cache ()
  "Run a gtklookup process and get a list of cache (db key)"

  (split-string
   (with-output-to-string
     (call-process gtklookup-program nil standard-output nil 
           "-d" (expand-file-name gtklookup-db-file)
           "-c"))))

(defun gtklookup-exec-lookup (search-term)
  "Runs a gtklookup process and returns a list of (term, url) pairs."

  (mapcar 
   (lambda (x) (split-string x "\t"))
   (split-string
     (with-output-to-string
         (call-process gtklookup-program nil standard-output nil 
                       "-d" (expand-file-name gtklookup-db-file) 
               "-l" search-term))
     "\n" t)))

(defun gtklookup-exec-all ()
  "Runs a gtklookup process and returns a list of all candidates"

  ;; (key, url, cat)
  (mapcar 
   (lambda (x) (split-string x "\t"))
   (split-string
     (with-output-to-string
         (call-process gtklookup-program nil standard-output nil 
                       "-d" (expand-file-name gtklookup-db-file) 
                       "-a"))
     "\n" t)))

;;=================================================================
;; interactive user interfaces
;;=================================================================

(defun gtklookup-get-candidate ()
  "Return ( display, url ) pairs"

  (if gtklookup-all
      gtklookup-all
    (setq gtklookup-all 
          (mapcar (lambda (x) (cons (format "%-40s : %5s" (car x) (caddr x)) (cadr x)))
                  (gtklookup-exec-all)))))

;;;###autoload
(defun gtklookup-get-cache ()
  "Fetching cache from gtklookup.py"

  (if gtklookup-cache 
      gtklookup-cache 
    (setq gtklookup-cache (gtklookup-exec-get-cache))))

(defvar anything-c-source-gtk
  '((name . "Gtk+")
    (candidates . gtklookup-get-candidate)
    (action . browse-url))
  "See GTK+ Reference")

;; (anything 'anything-c-source-gtk)

;;;###autoload
(defun gtklookup-lookup ()
  "Lookup SEARCH-TERM in the GTK+ Reference indexes."
  
  (interactive)
  (anything 'anything-c-source-gtk (symbol-at-point)))

;;;###autoload
(defun gtklookup-update (src)
  "Run gtklookup-update and create the database at `gtklookup-db-file'."
  (interactive)

  ;; gtklookup.py -d /home/taesoo/.gtklookup/gtklookup.db -u
  (call-process gtklookup-program nil standard-output nil 
                "-d" (expand-file-name gtklookup-db-file) 
                "-u"))

(provide 'gtklookup)
;;; gtklookup.el ends here
