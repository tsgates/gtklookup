;; 
;; gtk autoloader
;;

(eval-when-compile (require 'gtklookup))

(defvar gtklookup-dir ".")

;; set executable file and db file
(setq gtklookup-program (concat gtklookup-dir "/gtklookup.py"))
(setq gtklookup-db-file (concat gtklookup-dir "/gtklookup.db"))

;; to speedup, just load it on demand
(autoload 'gtklookup-lookup "gtklookup"
  "Lookup SEARCH-TERM in the GTK+ HTML indexes." t)

(autoload 'gtklookup-update "gtklookup" 
  "Run gtklookup-update and create the database at `gtklookup-db-file'." t)

(autoload 'gtklookup-get-cache "gtklookup"
  "Fetching cache from gtklookup.py" t)

(provide 'gtklookup-autoload)