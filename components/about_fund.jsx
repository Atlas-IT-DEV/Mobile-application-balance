import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { SvgXml } from "react-native-svg";
import { arrowDown, arrowLinkIcon, arrowUp } from "../images/images";
import { useState } from "react";

const AboutFund = () => {
  const [rows, setRows] = useState(2);
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>О фонде</Text>
        <TouchableOpacity style={styles.inviteButton}>
          <Text style={styles.inviteText}>Пригласить друзей</Text>
          <SvgXml xml={arrowLinkIcon} />
        </TouchableOpacity>
      </View>
      <View style={styles.mainInfo}>
        <Text numberOfLines={rows} style={styles.mainText}>
          Благотворительный фонд БАЛАНС. Мы помогаем тем, кто нуждается в жилье,
          расселении и ремонте. Вместе мы сила, давайте делать радость!
        </Text>
      </View>
      <TouchableOpacity
        style={styles.openTextButton}
        onPress={() => {
          rows == 2 ? setRows(null) : setRows(2);
        }}
      >
        <Text style={styles.openText}>Читать далее</Text>
        <SvgXml xml={rows == 2 ? arrowDown : arrowUp} />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 20,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 3,
      height: 3,
    },
    shadowOpacity: 0.7,
    shadowRadius: 2,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  headerText: {
    fontFamily: "IBMSemiBold",
    fontSize: 18,
    color: "rgba(22, 3, 111, 1)",
  },
  inviteButton: {
    flexDirection: "row",
    alignItems: "center",
    gap: 3,
    borderBottomColor: "rgba(22, 3, 111, 1)",
    borderBottomWidth: 2,
  },
  inviteText: {
    color: "rgba(22, 3, 111, 1)",
    fontFamily: "IBMMedium",
    fontSize: 12,
  },
  mainInfo: {
    marginTop: 10,
  },
  mainText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMRegular",
    fontSize: 12,
  },
  openTextButton: {
    marginTop: 10,
    flexDirection: "row",
    alignItems: "center",
    gap: 2,
  },
  openText: {
    fontSize: 12,
    fontFamily: "IBMMedium",
    color: "rgba(22, 3, 111, 1)",
  },
});

export default AboutFund;
