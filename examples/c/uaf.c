/* Example for the C checks: a use-after-free that compiles cleanly. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    int qty;
} Item;

static Item *item_new(const char *name, int qty) {
    Item *item = malloc(sizeof *item);
    if (item == NULL) return NULL;
    item->name = strdup(name);
    if (item->name == NULL) {
        free(item);
        return NULL;
    }
    item->qty = qty;
    return item;
}

static void item_free(Item *item) {
    free(item->name);
    free(item);
}

int main(void) {
    Item *item = item_new("widget", 3);
    if (item == NULL) return 1;

    item_free(item);
    printf("%s x%d\n", item->name, item->qty); /* use-after-free */
    return 0;
}
