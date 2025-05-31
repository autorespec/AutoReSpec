public class EntryList {
    Object first;
    EntryList rest;
    EntryList(Object first, EntryList rest) {
        this.first = first;
        this.rest = rest;
    }

    public int size() {
        if(this.first == null) {
            return 0;
        }
        if(this.rest == null) {
            return 1;
        } else {
            return 1 + rest.size();
        }
    }

}
