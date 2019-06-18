{{- define "caas.protocol_parser" }}
{{- $url :=  regexSplit ":" . -1 }}
       protocol {{ index $url 0 }}
{{- end }}
{{- define "caas.scheme_parser" }}
{{- $url :=  regexSplit ":" . -1 }}
       scheme {{ index $url 0 }}
{{- end }}
{{- define "caas.url_parser" }}
{{- $url :=  regexSplit ":" . -1 }}
{{- $just_url :=  index $url 1 }}
{{- $just_url :=  regexSplit "\\/\\/" $just_url -1 }}
       host {{ index $just_url 1 }}
       port {{ index $url 2 }}
{{- end }}