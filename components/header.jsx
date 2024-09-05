import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { SvgXml } from "react-native-svg";

import { logo, tgIcon, vkIcon, whatsappIcon } from "../images/images";

const Header = () => {
  return (
    <View style={styles.container}>
      <View>
        <SvgXml xml={logo} />
        <Text style={styles.fondText}>Благотворительный фонд </Text>
      </View>
      <View style={styles.connect}>
        <TouchableOpacity>
          <SvgXml xml={whatsappIcon} />
        </TouchableOpacity>
        <TouchableOpacity>
          <SvgXml xml={vkIcon} />
        </TouchableOpacity>
        <TouchableOpacity>
          <SvgXml xml={tgIcon} />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  fondText: {
    fontFamily: "IBMMedium",
    fontSize: 11,
    color: "rgba(45, 22, 153, 1)",
  },
  connect: {
    flexDirection: "row",
    gap: 15,
  },
});

export default Header;
