import { useEffect, useState } from "react";

import Grid from "@mui/material/Grid2";


import ItemList from "./components/list";
import ActionSelect from "./components/select";
import { Item } from "./datatypes";
import axios from "axios";
import { Box } from "@mui/material";
import SearchBar from "./components/search";
import ItemCard from "./components/card";

const height: string = "86vh"
const leftCol: number = 3.5;

export const border: string = 'solid #D3D3D3 1px';

export default function Mobile() {
        const [data, setData] = useState<Array<Item>>([])
        const [items, setItems] = useState<Array<Item>>([])
        const [searchHeight, setSearchHeight] = useState<string>("73px");
        const [item, setItem] = useState<Item | null>(null)


        // динамичное изменение размера
        const handleResize = () => {
                const h = document.querySelector("#searchRow");
                const sh = h ? getComputedStyle(h).getPropertyValue("height") : searchHeight;
                setSearchHeight(sh);
        };
        window.addEventListener("resize", handleResize)


        useEffect(() => {
                axios.post("http://127.0.0.1:1234/example/1014",
                        { scheme: 10, iql: "Name LIKE !test" })
                        .then((response) => { setItems(response.data) });

        }, [])

        return (
                <>
                        <Box textAlign={"left"} sx={{ boxShadow: 8, height: height, width: "84vw" }}>

                                <Grid container id="searchRow" sx={{ borderBottom: border }} size={12}>
                                        <Grid size={leftCol} p={1}
                                                sx={{ borderRight: border }} >
                                                <ActionSelect />
                                        </Grid>
                                        <Grid size={12 - leftCol} p={1}>
                                                <SearchBar />
                                        </Grid>
                                </Grid>
                                <Grid container size={12}>
                                        <Grid size={leftCol}
                                                sx={{
                                                        height: `calc(${height} - ${searchHeight})`,
                                                        borderRight: border,
                                                        overflowY: "auto",
                                                        scrollbarWidth: "none"
                                                }}>
                                                <ItemList items={items} setParentItem={setItem} /></Grid>
                                        <Grid size={12 - leftCol}>
                                                {item && <ItemCard item={item} />}
                                        </Grid>

                                </Grid>
                        </Box>
                </>)
}
