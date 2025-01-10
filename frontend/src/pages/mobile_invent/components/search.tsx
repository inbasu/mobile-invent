import TextField from '@mui/material/TextField';
import { Item } from "../datatypes";
import { useContext, useEffect, useState } from 'react';
import { ActionContext, ItemsContext, ResultContext, ItemContext, LoadingContext, StoreContext, DataContext, QuerryContext } from '../context';

import axios from "axios";
import { actionFilter, querryFilter } from '../search';


const searchFilter = (
        items: Array<Item>,
        fields: Array<string>,
        querry: string,
) => {
        return items.filter(item => {
                for (const attr of item.attrs) {
                        if (fields.includes(attr.name) && (attr.values[0].label.toLowerCase().includes(querry.toLowerCase()))) {
                                return true;
                        }
                }
                return false;
        })
}



export default function SearchBar() {
        const [action, _setAction] = useContext(ActionContext);
        const [_data, setData] = useContext(DataContext);
        const [items, setItems] = useContext(ItemsContext);
        const [_results, setResults] = useContext(ResultContext);
        const [_item, setItem] = useContext(ItemContext);
        const [loading, setLoading] = useContext(LoadingContext);
        const [store, _setStore] = useContext(StoreContext);
        const [querry, setQuerry] = useContext(QuerryContext);

        const [label, setLabel] = useState<string>('');

        useEffect(() => {
                if (action === "takeback") {
                        setLabel('3.Введите номер оборудования или фамилию пользователя(на английском)')
                } else if (action === "giveaway") {
                        setLabel("3.Введите номер реквеста или фамилию пользователя(на английском)")
                } else { setLabel('') }
        }, [action])


        useEffect(() => {
                if (store !== "IT") {
                        setResults(querryFilter(items, querry));
                } else if (store === "IT" && querry.length > 3) {
                        setLoading(true);
                        axios.post('http://127.0.0.1:8800/mobile/items/it/', { querry: querry })
                                .then((response) => {
                                        setData(response.data);
                                        setResults(actionFilter(response.data, action, store));
                                        setResults(actionFilter(response.data, action, store));
                                })
                                .finally(() => { setLoading(false) })
                }
        }, [querry])


        return (
                <TextField id="search-bar"
                        onChange={event => setQuerry(event.target.value)}
                        value={querry}
                        label={label}
                        fullWidth
                        disabled={loading || !label} />
        )
}
