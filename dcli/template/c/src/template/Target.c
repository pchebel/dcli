#include "Target.h"
#include <stdbool.h>

// Executed when you Run your code
void run() {
}

{{ targetMethodReturn }} {{ targetMethod }}({{ targetMethodArgs }}) {
    //TODO implement what the user will get for the first time.
    {% for var in targetVariableInitializations%}
    {{ var.type }} {{ var.name }};
    {% endfor %}
    {% if targetMethodReturn != "" %}return {{ targetMethodReturnValue }};{% endif %}
}