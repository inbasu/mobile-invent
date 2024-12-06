import Grid from "@mui/material/Grid2";
import { Item, Values } from "../datatypes"
import ButtonGroup from "./buttonsGrp";


const hardwareFields = (action: string) => {
        switch (action) {
                case "takeback":
                        return ["INV No", "Serial No", "Model", "State", "Location", "User"];
                case "giveaway":
                        return [];
                default:
                        return [];

        }
}

const ereqFields = ['Кто принял', 'Дата сдачи', "Кто выдал", , 'Дата выдачи', "Пользователь"]



const AttrRow = ({ attr }: { attr: Values }) => {
        return (
                <>
                        <Grid size={4}>{attr.name}:</Grid>
                        <Grid size={8}>{attr.values[0] ? attr.values[0].label : ''}</Grid>
                </>)
}

export default function ItemCard({ item }: { item: Item }) {
        const action: string = "takeback"
        return (
                <Grid container p={2}>
                        <Grid size={12}><h3>{item.label}</h3></Grid>
                        <Grid container size={12} pb={3}>
                                {item.attrs && item.attrs.map(attr => {
                                        if (hardwareFields(action).includes(attr.name) && attr.values) {
                                                return (<AttrRow attr={attr} />)
                                        }
                                })}
                        </Grid>
                        <Grid container size={12} pb={3}>
                                {item.ereq && item.ereq?.attrs?.map(attr => {
                                        if (ereqFields.includes(attr.name)) {
                                                return (<AttrRow attr={attr} />)

                                        }
                                })}
                        </Grid>
                        <Grid size={12}>
                                <ButtonGroup action={action} item={item} />
                        </Grid>
                </Grid>)
}
